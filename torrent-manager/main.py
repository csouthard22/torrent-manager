import logging
from qbittorrentapi import Client
import time
import os
from typing import List, Dict, Any

from .config import load_config
from .torrent_manager import TorrentManager
from .notification import send_notification
from .logger import setup_logging

class QBittorrentCleanupTool:
    def __init__(self, config_path: str = 'config.yaml'):
        # Load configuration
        self.config = load_config(config_path)
        
        # Setup logging
        self.logger = setup_logging(self.config['log_path'])
        
        # Initialize qBittorrent client
        try:
            self.client = Client(
                host=self.config['qbittorrent']['host'],
                port=self.config['qbittorrent']['port'],
                username=self.config['qbittorrent']['username'],
                password=self.config['qbittorrent']['password']
            )
            self.client.auth_log_in()
        except Exception as e:
            self.logger.error(f"Failed to connect to qBittorrent: {e}")
            raise
        
        # Initialize torrent manager
        self.torrent_manager = TorrentManager(
            self.client, 
            self.config, 
            self.logger
        )
    
    def run(self):
        """Main run method for the cleanup tool"""
        try:
            # Find torrents without hardlinks
            torrents_to_check = self.torrent_manager.find_torrents_without_hardlinks()
            
            # Process each torrent
            for torrent in torrents_to_check:
                try:
                    # Check if torrent meets deletion criteria
                    if self.torrent_manager.is_torrent_deletable(torrent):
                        # Mark for deletion or delete based on config
                        self.handle_torrent_deletion(torrent)
                except Exception as e:
                    self.logger.error(f"Error processing torrent {torrent.hash}: {e}")
        
        except Exception as e:
            self.logger.error(f"Unexpected error in cleanup process: {e}")
            send_notification(f"Cleanup tool error: {e}", self.config)
    
    def handle_torrent_deletion(self, torrent):
        """Handle torrent deletion based on configuration"""
        if self.config['deletion_mode'] == 'manual':
            # Add a tag for manual deletion
            self.client.torrents_add_tags(
                torrent_hashes=[torrent.hash], 
                tags=['to_delete']
            )
            send_notification(
                f"Torrent {torrent.name} marked for manual deletion", 
                self.config
            )
        
        elif self.config['deletion_mode'] == 'automatic':
            # Check if torrent has been marked long enough
            if self.torrent_manager.is_ready_for_automatic_deletion(torrent):
                # Delete the torrent
                self.client.torrents_delete(
                    torrent_hashes=[torrent.hash], 
                    delete_files=True
                )
                send_notification(
                    f"Torrent {torrent.name} automatically deleted", 
                    self.config
                )
                self.logger.info(f"Deleted torrent: {torrent.name}")

def main():
    cleanup_tool = QBittorrentCleanupTool()
    
    # Run periodically
    while True:
        cleanup_tool.run()
        time.sleep(cleanup_tool.config['check_interval'])

if __name__ == '__main__':
    main()