class ShipmentTracker:
    def __init__(self):
        self.shipments = {}
    
    def add_shipment(self, tracking_id, destination, status):
        """Add new shipment to tracking system"""
        self.shipments[tracking_id] = {
            'destination': destination,
            'status': status,
            'updates': []
        }
        return f"Shipment {tracking_id} added successfully"
    
    def get_shipment_status(self, tracking_id):
        """Get current status of shipment"""
        if tracking_id in self.shipments:
            return self.shipments[tracking_id]
        return "Shipment not found"
    
    def update_status(self, tracking_id, new_status):
        """Update shipment status"""
        if tracking_id in self.shipments:
            self.shipments[tracking_id]['status'] = new_status
            self.shipments[tracking_id]['updates'].append(new_status)
            return f"Status updated to: {new_status}"
        return "Shipment not found"

    def get_realtime_location(self, tracking_id):
        """Get real-time GPS location of shipment"""
        if tracking_id in self.shipments:
            # Simulasi koordinat GPS
            return {
                'tracking_id': tracking_id,
                'latitude': 1.3521,
                'longitude': 103.8198,
                'last_update': '2024-12-18 10:30:00',
                'current_location': 'Singapore Port'
            }
        return "Shipment not found"
    
    def get_estimated_arrival(self, tracking_id):
        """Calculate estimated arrival time"""
        if tracking_id in self.shipments:
            return {
                'tracking_id': tracking_id,
                'estimated_arrival': '2024-12-25 14:00:00',
                'status': 'In Transit'
            }
        return "Shipment not found"

# Main execution
if __name__ == "__main__":
    tracker = ShipmentTracker()
    print(tracker.add_shipment("TRK001", "Singapore", "Processing"))
    print(tracker.get_shipment_status("TRK001"))
    