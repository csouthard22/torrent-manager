import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

class TorrentManager:
    def __init__(self, client, config, logger):
        self.client = client
        self.config = config
        self.logger = logger
    
    def find_torrents_without_hardlinks(self) -> List[Any]:
        """Find torrents without hardlinks"""
        torrents = []
        for torrent in self.client.torrents_info():
            # Check if torrent has multiple hardlinks
            save_path = torrent.save_path
            torrent_files = self.client.torrents_files(torrent.hash)
            
            # Check if any file in torrent has multiple hardlinks
            has_hardlinks = any(
                self._count_hardlinks(os.path.join(save_path, file['name'])) > 1 
                for file in torrent_files
            )
            
            if not has_hardlinks:
                torrents.append(torrent)
        
        return torrents
    
    def _count_hardlinks(self, filepath: str) -> int:
        """Count hardlinks for a given file"""
        try:
            return os.stat(filepath).st_nlink
        except Exception as e:
            self.logger.error(f"Error counting hardlinks for {filepath}: {e}")
            return 0
    
    def is_torrent_deletable(self, torrent) -> bool:
        """Check if torrent meets deletion criteria"""
        # Check ignore list
        if torrent.name in self.config.get('ignore_list', []):
            return False
        
        # Check seeding time by tracker
        tracker = self._get_primary_tracker(torrent)
        min_seed_time = self.config.get('tracker_seed_times', {}).get(tracker, 0)
        
        # Compare actual seed time with minimum required
        return (
            torrent.seeding_time >= min_seed_time and 
            torrent.ratio >= self.config.get('minimum_ratio', 1.0)
        )
    
    def _get_primary_tracker(self, torrent) -> str:
        """Extract primary tracker from torrent"""
        trackers = self.client.torrents_trackers(torrent.hash)
        # Logic to determine primary tracker (first working tracker)
        for tracker in trackers:
            if tracker['status'] == 2:  # Working tracker
                return tracker['url']
        return 'default'
    
    def is_ready_for_automatic_deletion(self, torrent) -> bool:
        """Check if torrent is ready for automatic deletion"""
        # Check if torrent has been marked for deletion for configured days
        marked_time = torrent.added_on  # or use a custom tag's timestamp
        days_marked = (datetime.now() - datetime.fromtimestamp(marked_time)).days
        
        return days_marked >= self.config.get('deletion_delay_days', 30)