class ShipmentTracker:
    def __init__(self):
        self.shipments = {}
    
    def add_shipment(self, tracking_id, destination, status):
        """Add new shipment to tracking system with validation"""
        # Validasi: tracking_id tidak boleh kosong
        if not tracking_id or tracking_id.strip() == "":
            return "Error: Tracking ID cannot be empty"
        
        # Validasi: tracking_id harus unique
        if tracking_id in self.shipments:
            return f"Error: Shipment {tracking_id} already exists"
        
        # Validasi: destination tidak boleh kosong
        if not destination or destination.strip() == "":
            return "Error: Destination cannot be empty"
            
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

# Main execution
if __name__ == "__main__":
    tracker = ShipmentTracker()
    print(tracker.add_shipment("TRK001", "Singapore", "Processing"))
    print(tracker.get_shipment_status("TRK001"))
    