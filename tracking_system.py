import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Union
from email_service import EmailNotificationService

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
        """Update shipment status with email notification"""
        if tracking_id in self.shipments:
            self.shipments[tracking_id]['status'] = new_status
            self.shipments[tracking_id]['updates'].append(new_status)
            
            # Send email notification if email provided
            if notify_email:
                email_service = EmailNotificationService()
                email_service.send_status_update(tracking_id, notify_email, new_status)
            
            return f"Status updated to: {new_status}"
        return "Shipment not found"

    def get_realtime_location(self, tracking_id: str) -> Union[Dict, str]:
        """
        Get real-time GPS location of shipment
        
        Args:
            tracking_id (str): The tracking ID of the shipment
            
        Returns:
            dict: Location data with coordinates
            str: Error message if tracking_id not found or invalid
            
        Raises:
            ValueError: If coordinates are invalid
        """
        # Error Handling 1: Validate tracking_id exists
        if not tracking_id or tracking_id.strip() == "":
            return {
                'error': 'Invalid tracking ID',
                'message': 'Tracking ID cannot be empty'
            }
        
        if tracking_id not in self.shipments:
            return {
                'error': 'Shipment not found',
                'message': f'No shipment found with ID: {tracking_id}'
            }
        
        try:
            # Simulasi GPS coordinates
            # Dalam implementasi real, ini akan fetch dari GPS device/API
            latitude = 1.3521
            longitude = 103.8198
            
            # Error Handling 2: Validate GPS coordinates
            if not self._validate_coordinates(latitude, longitude):
                return {
                    'error': 'Invalid GPS coordinates',
                    'message': 'GPS coordinates are out of valid range',
                    'tracking_id': tracking_id
                }
            
            # Error Handling 3: Check if shipment is in valid status for tracking
            current_status = self.shipments[tracking_id]['status']
            if current_status in ['Delivered', 'Cancelled', 'Returned']:
                return {
                    'warning': 'Shipment not in transit',
                    'message': f'Shipment status is {current_status}. Real-time tracking not available.',
                    'tracking_id': tracking_id,
                    'status': current_status
                }
            
            # Get location name based on coordinates
            location_name = self._get_location_name(latitude, longitude)
            
            # Add timezone information
            timezone = self._get_timezone_for_location(latitude, longitude)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return {
                'tracking_id': tracking_id,
                'latitude': latitude,
                'longitude': longitude,
                'current_location': location_name,
                'last_update': current_time,
                'timezone': timezone,
                'accuracy': 'high',  # GPS accuracy indicator
                'status': 'active'
            }
            
        except ValueError as ve:
            # Error Handling 4: Handle value errors
            return {
                'error': 'Value Error',
                'message': str(ve),
                'tracking_id': tracking_id
            }
        except Exception as e:
            # Error Handling 5: Catch any unexpected errors
            return {
                'error': 'Unexpected Error',
                'message': f'An error occurred while retrieving location: {str(e)}',
                'tracking_id': tracking_id
            }
    
    def get_estimated_arrival(self, tracking_id: str) -> Union[Dict, str]:
        """
        Calculate estimated arrival time
        
        Args:
            tracking_id (str): The tracking ID of the shipment
            
        Returns:
            dict: ETA information
            str: Error message if tracking_id not found
        """
        # Error Handling 1: Validate tracking_id
        if not tracking_id or tracking_id.strip() == "":
            return {
                'error': 'Invalid tracking ID',
                'message': 'Tracking ID cannot be empty'
            }
        
        if tracking_id not in self.shipments:
            return {
                'error': 'Shipment not found',
                'message': f'No shipment found with ID: {tracking_id}'
            }
        
        try:
            shipment = self.shipments[tracking_id]
            current_status = shipment['status']
            
            # Error Handling 2: Check if ETA is applicable
            if current_status == 'Delivered':
                return {
                    'tracking_id': tracking_id,
                    'status': 'Delivered',
                    'message': 'Shipment has already been delivered',
                    'delivered_at': shipment.get('delivered_at', 'N/A')
                }
            
            if current_status == 'Cancelled':
                return {
                    'tracking_id': tracking_id,
                    'status': 'Cancelled',
                    'message': 'Shipment has been cancelled. No ETA available.'
                }
            
            # Error Handling 3: Validate destination exists
            destination = shipment.get('destination')
            if not destination:
                return {
                    'error': 'Missing destination',
                    'message': 'Cannot calculate ETA without destination',
                    'tracking_id': tracking_id
                }
            
            # Calculate ETA based on destination and current status
            eta_days = self._calculate_eta_days(destination, current_status)
            
            # Error Handling 4: Validate ETA calculation
            if eta_days is None or eta_days < 0:
                return {
                    'error': 'ETA calculation failed',
                    'message': 'Unable to calculate estimated arrival time',
                    'tracking_id': tracking_id
                }
            
            estimated_arrival = datetime.now() + timedelta(days=eta_days)
            
            # Add timezone for destination
            destination_timezone = self._get_timezone_for_destination(destination)
            
            return {
                'tracking_id': tracking_id,
                'destination': destination,
                'current_status': current_status,
                'estimated_arrival': estimated_arrival.strftime('%Y-%m-%d %H:%M:%S'),
                'timezone': destination_timezone,
                'days_remaining': eta_days,
                'confidence_level': 'high' if current_status == 'In Transit' else 'medium'
            }
            
        except ValueError as ve:
            return {
                'error': 'Value Error',
                'message': str(ve),
                'tracking_id': tracking_id
            }
        except Exception as e:
            return {
                'error': 'Unexpected Error',
                'message': f'An error occurred while calculating ETA: {str(e)}',
                'tracking_id': tracking_id
            }
    
    # Helper Methods untuk Error Handling
    
    def _validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        Validate GPS coordinates are within valid ranges
        
        Args:
            latitude: Latitude value (-90 to 90)
            longitude: Longitude value (-180 to 180)
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
            
            # Valid ranges: latitude [-90, 90], longitude [-180, 180]
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return True
            return False
        except (ValueError, TypeError):
            return False
    
    def _get_location_name(self, latitude: float, longitude: float) -> str:
        """
        Get location name from coordinates (simplified version)
        In production, this would use reverse geocoding API
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            str: Location name
        """
        # Simplified mapping for demo purposes
        location_map = {
            (1.3521, 103.8198): 'Singapore Port',
            (22.3193, 114.1694): 'Hong Kong International Terminal',
            (-6.2088, 106.8456): 'Jakarta Tanjung Priok Port',
            (3.1390, 101.6869): 'Kuala Lumpur Distribution Center'
        }
        
        # Find closest location (simplified)
        for coords, name in location_map.items():
            if abs(coords[0] - latitude) < 0.1 and abs(coords[1] - longitude) < 0.1:
                return name
        
        return f"Location ({latitude:.4f}, {longitude:.4f})"
    
    def _get_timezone_for_location(self, latitude: float, longitude: float) -> str:
        """
        Get timezone based on coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            str: Timezone string
        """
        # Simplified timezone mapping
        if 100 <= longitude <= 110:
            return 'GMT+7 (WIB)'
        elif 103 <= longitude <= 105:
            return 'GMT+8 (SGT)'
        elif 113 <= longitude <= 115:
            return 'GMT+8 (HKT)'
        else:
            return 'GMT+0 (UTC)'
    
    def _get_timezone_for_destination(self, destination: str) -> str:
        """
        Get timezone for destination country/city
        
        Args:
            destination: Destination name
            
        Returns:
            str: Timezone string
        """
        timezone_map = {
            'Singapore': 'GMT+8 (SGT)',
            'Hong Kong': 'GMT+8 (HKT)',
            'Jakarta': 'GMT+7 (WIB)',
            'Malaysia': 'GMT+8 (MYT)',
            'Thailand': 'GMT+7 (ICT)',
            'Vietnam': 'GMT+7 (ICT)',
            'Philippines': 'GMT+8 (PHT)'
        }
        
        for country, tz in timezone_map.items():
            if country.lower() in destination.lower():
                return tz
        
        return 'GMT+0 (UTC)'
    
    def _calculate_eta_days(self, destination: str, current_status: str) -> Optional[int]:
        """
        Calculate estimated days to arrival based on destination and status
        
        Args:
            destination: Destination country/city
            current_status: Current shipment status
            
        Returns:
            int: Number of days until arrival, or None if cannot calculate
        """
        # Base transit days by destination
        transit_days = {
            'Singapore': 2,
            'Hong Kong': 3,
            'Malaysia': 2,
            'Thailand': 4,
            'Vietnam': 5,
            'Philippines': 4,
            'Jakarta': 3,
            'Kuala Lumpur': 2
        }
        
        # Status multipliers
        status_modifiers = {
            'Processing': 1.5,      # Still in warehouse
            'In Transit': 1.0,      # On the way
            'Customs Clearance': 1.2,  # Delayed by customs
            'Out for Delivery': 0.1    # Almost there
        }
        
        # Find base days
        base_days = None
        for dest, days in transit_days.items():
            if dest.lower() in destination.lower():
                base_days = days
                break
        
        if base_days is None:
            base_days = 7  # Default for unknown destinations
        
        # Apply status modifier
        modifier = status_modifiers.get(current_status, 1.0)
        
        estimated_days = int(base_days * modifier)
        
        return estimated_days if estimated_days >= 0 else None

# Main execution
if __name__ == "__main__":
    tracker = ShipmentTracker()
    print(tracker.add_shipment("TRK001", "Singapore", "Processing"))
    print(tracker.get_shipment_status("TRK001"))
    