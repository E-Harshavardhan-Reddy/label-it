"""
Enhanced geolocation service with professional UI components
"""

import streamlit as st
import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class GeolocationManager:
    """Professional geolocation manager with enhanced UI"""
    
    def __init__(self):
        self.location_cache = {}
    
    def get_ip_location(self) -> Optional[Dict]:
        """Get location from IP with enhanced error handling"""
        # Check session cache first
        if 'ip_location_cache' in st.session_state:
            return st.session_state.ip_location_cache
        
        try:
            # Primary service: ipapi.co
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('latitude') and data.get('longitude'):
                    location = {
                        'latitude': float(data.get('latitude')),
                        'longitude': float(data.get('longitude')),
                        'city': data.get('city'),
                        'country': data.get('country_name'),
                        'method': 'IP',
                        'accuracy': 10000,
                        'service': 'ipapi.co'
                    }
                    st.session_state.ip_location_cache = location
                    return location
        except Exception as e:
            logger.warning(f"Primary IP location service failed: {e}")
        
        # Fallback service
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('lat') and data.get('lon'):
                    location = {
                        'latitude': float(data.get('lat')),
                        'longitude': float(data.get('lon')),
                        'city': data.get('city'),
                        'country': data.get('country'),
                        'method': 'IP',
                        'accuracy': 10000,
                        'service': 'ip-api.com'
                    }
                    st.session_state.ip_location_cache = location
                    return location
        except Exception as e:
            logger.warning(f"Fallback IP location service failed: {e}")
        
        return None
    
    def render_manual_input(self) -> Optional[Dict]:
        """Professional manual coordinate input interface"""
        st.markdown("### 📍 Manual Location Entry")
        st.info("💡 Enter precise coordinates for accurate location tagging")
        
        col1, col2 = st.columns(2)
        
        with col1:
            latitude = st.number_input(
                "🌐 Latitude",
                min_value=-90.0,
                max_value=90.0,
                value=0.0,
                format="%.6f",
                help="Latitude: -90 (South Pole) to +90 (North Pole)",
                key="manual_lat"
            )
        
        with col2:
            longitude = st.number_input(
                "🌐 Longitude",
                min_value=-180.0,
                max_value=180.0,
                value=0.0,
                format="%.6f",
                help="Longitude: -180 to +180",
                key="manual_lon"
            )
        
        # Professional examples section
        with st.expander("📍 Popular Locations"):
            st.markdown("**🇮🇳 Major Indian Cities:**")
            
            cities = [
                ("Mumbai", 19.0760, 72.8777),
                ("Delhi", 28.7041, 77.1025),
                ("Bangalore", 12.9716, 77.5946),
                ("Chennai", 13.0827, 80.2707),
                ("Kolkata", 22.5726, 88.3639),
                ("Hyderabad", 17.3850, 78.4867),
                ("Pune", 18.5204, 73.8567),
                ("Ahmedabad", 23.0225, 72.5714)
            ]
            
            for city, lat, lon in cities:
                if st.button(f"📍 {city} ({lat:.4f}, {lon:.4f})", key=f"city_{city}"):
                    st.session_state.manual_lat = lat
                    st.session_state.manual_lon = lon
                    st.rerun()
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Use Coordinates", type="primary", use_container_width=True):
                if latitude != 0.0 or longitude != 0.0:
                    location = {
                        'latitude': latitude,
                        'longitude': longitude,
                        'method': 'Manual',
                        'accuracy': 1  # Very precise
                    }
                    
                    # Try reverse geocoding
                    try:
                        reverse_info = self.reverse_geocode(latitude, longitude)
                        if reverse_info:
                            location.update(reverse_info)
                    except Exception:
                        pass
                    
                    return location
                else:
                    st.warning("⚠️ Please enter non-zero coordinates")
        
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.manual_lat = 0.0
                st.session_state.manual_lon = 0.0
                st.rerun()
        
        with col3:
            if latitude != 0.0 and longitude != 0.0:
                maps_url = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}&zoom=12"
                st.link_button("🗺️ Preview", maps_url, use_container_width=True)
        
        return None
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """Get address information from coordinates"""
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1,
                'zoom': 10
            }
            headers = {'User-Agent': 'LabelIt-Professional/1.0 (Educational)'}
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                
                return {
                    'city': (address.get('city') or 
                            address.get('town') or 
                            address.get('village') or 
                            address.get('hamlet') or
                            address.get('suburb')),
                    'country': address.get('country'),
                    'state': address.get('state'),
                    'display_name': data.get('display_name', '')[:100]
                }
        except Exception as e:
            logger.warning(f"Reverse geocoding failed: {e}")
        
        return None
    
    def display_location_widget_in_form(self) -> Optional[Dict]:
        """Form-compatible location capture widget"""
        st.markdown("### 🌍 Location Information")
        st.markdown("📍 Adding location helps organize images geographically and improves discoverability")
        
        # Initialize session state
        if 'location_data' not in st.session_state:
            st.session_state.location_data = None
        
        # Professional method selection
        method = st.radio(
            "**Choose location method:**",
            ["🌐 Use IP Location", "📝 Manual Entry", "❌ No Location"],
            horizontal=True,
            help="IP location is quick but approximate. Manual entry provides precise coordinates."
        )
        
        location_data = None
        
        if method == "🌐 Use IP Location":
            st.info("🌐 Will automatically detect location from your internet connection when submitted")
            # Show cached location if available
            if 'ip_location_cache' in st.session_state:
                cached_location = st.session_state.ip_location_cache
                st.success(f"📍 Cached location: {cached_location.get('city', 'Unknown')}, {cached_location.get('country', 'Unknown')}")
                location_data = cached_location
            else:
                st.caption("Location will be detected automatically during upload")
                # Pre-fetch IP location for form submission
                ip_location = self.get_ip_location()
                if ip_location:
                    location_data = ip_location
        
        elif method == "📝 Manual Entry":
            st.markdown("**Manual Coordinates:**")
            
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input(
                    "🌐 Latitude",
                    min_value=-90.0,
                    max_value=90.0,
                    value=st.session_state.get('manual_lat', 0.0),
                    format="%.6f",
                    help="Latitude: -90 (South Pole) to +90 (North Pole)",
                    key="form_manual_lat"
                )
            
            with col2:
                longitude = st.number_input(
                    "🌐 Longitude",
                    min_value=-180.0,
                    max_value=180.0,
                    value=st.session_state.get('manual_lon', 0.0),
                    format="%.6f",
                    help="Longitude: -180 to +180",
                    key="form_manual_lon"
                )
            
            if latitude != 0.0 or longitude != 0.0:
                location_data = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'method': 'Manual',
                    'accuracy': 1
                }
                
                # Try reverse geocoding
                try:
                    reverse_info = self.reverse_geocode(latitude, longitude)
                    if reverse_info:
                        location_data.update(reverse_info)
                except Exception:
                    pass
        
        elif method == "❌ No Location":
            st.info("📍 No location will be added to this image")
            location_data = None
        
        # Display current location selection
        if location_data:
            st.success("📍 Location ready for upload:")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Latitude", f"{location_data.get('latitude', 0):.6f}")
            with col2:
                st.metric("Longitude", f"{location_data.get('longitude', 0):.6f}")
            
            if location_data.get('city') and location_data.get('country'):
                st.caption(f"📍 {location_data.get('city')}, {location_data.get('country')}")
        
        return location_data
    
    def display_location_widget(self) -> Optional[Dict]:
        """Professional location capture widget for non-form contexts"""
        st.markdown("### 🌍 Location Information")
        st.markdown("📍 Adding location helps organize images geographically and improves discoverability")
        
        # Initialize session state
        if 'location_data' not in st.session_state:
            st.session_state.location_data = None
        
        # Professional method selection
        method = st.radio(
            "**Choose location method:**",
            ["🌐 Automatic (IP-based)", "📝 Manual Entry"],
            horizontal=True,
            help="IP location is quick but approximate. Manual entry provides precise coordinates."
        )
        
        location_data = None
        
        if method == "🌐 Automatic (IP-based)":
            st.info("🌐 Automatically detect location from your internet connection")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button("🎯 Detect Location", type="primary", use_container_width=True):
                    with st.spinner("🔍 Detecting your location..."):
                        location_data = self.get_ip_location()
                        if location_data:
                            st.session_state.location_data = location_data
                            st.success("✅ Location detected successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Unable to detect location. Please try manual entry.")
            
            with col2:
                if st.session_state.location_data and st.button("🔄 Refresh", use_container_width=True):
                    if 'ip_location_cache' in st.session_state:
                        del st.session_state.ip_location_cache
                    st.session_state.location_data = None
                    st.rerun()
        
        elif method == "📝 Manual Entry":
            location_data = self.render_manual_input()
            if location_data:
                st.session_state.location_data = location_data
                st.success("✅ Manual coordinates set successfully!")
        
        # Display current location with professional styling
        if st.session_state.location_data:
            self.display_location_info(st.session_state.location_data)
            
            # Professional action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Update Location", use_container_width=True):
                    st.session_state.location_data = None
                    if 'ip_location_cache' in st.session_state:
                        del st.session_state.ip_location_cache
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Remove Location", use_container_width=True):
                    st.session_state.location_data = None
                    if 'ip_location_cache' in st.session_state:
                        del st.session_state.ip_location_cache
                    st.rerun()
            
            with col3:
                if st.session_state.location_data.get('latitude') and st.session_state.location_data.get('longitude'):
                    lat = st.session_state.location_data['latitude']
                    lon = st.session_state.location_data['longitude']
                    maps_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=12"
                    st.link_button("🗺️ View on Map", maps_url, use_container_width=True)
        
        return st.session_state.location_data
    
    def display_location_info(self, location_data: Dict):
        """Display professional location information"""
        st.success("📍 Location Information Captured")
        
        # Professional metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lat = location_data.get('latitude', 0)
            st.metric(
                "🌐 Latitude",
                f"{lat:.6f}",
                help="Distance north (+) or south (-) of the equator"
            )
        
        with col2:
            lon = location_data.get('longitude', 0)
            st.metric(
                "🌐 Longitude",
                f"{lon:.6f}",
                help="Distance east (+) or west (-) of the Prime Meridian"
            )
        
        with col3:
            method = location_data.get('method', 'Unknown')
            accuracy = location_data.get('accuracy')
            
            if accuracy:
                if accuracy <= 100:
                    accuracy_text = f"🟢 High ({accuracy:.0f}m)"
                elif accuracy <= 1000:
                    accuracy_text = f"🟡 Medium ({accuracy:.0f}m)"
                else:
                    accuracy_text = f"🔴 Low ({accuracy/1000:.1f}km)"
            else:
                accuracy_text = f"📍 {method}"
            
            st.metric(
                "🎯 Accuracy",
                accuracy_text,
                help="Location precision estimate"
            )
        
        # Additional location details
        if location_data.get('city') or location_data.get('country'):
            st.markdown("**📍 Address Information:**")
            address_parts = []
            if location_data.get('city'):
                address_parts.append(f"🏙️ {location_data['city']}")
            if location_data.get('state'):
                address_parts.append(f"🗺️ {location_data['state']}")
            if location_data.get('country'):
                address_parts.append(f"🇮🇳 {location_data['country']}")
            
            if address_parts:
                st.info(" • ".join(address_parts))
        
        # Accuracy information
        if location_data.get('method') == 'IP':
            st.caption("ℹ️ IP-based location provides city-level accuracy (typically 5-50km radius)")
        elif location_data.get('method') == 'Manual':
            st.caption("ℹ️ Manual coordinates provide precise location (meter-level accuracy)")

# Global geolocation manager instance
geo_manager = GeolocationManager()
