"""
Professional utility functions for image processing and validation with enhanced features
"""

import io
import os
import re
from PIL import Image, ImageOps, ExifTags
import streamlit as st
from typing import Tuple, Optional, Union
import hashlib

def compress_image(uploaded_file, max_size=(1200, 1200), quality=85) -> io.BytesIO:
    """
    Professional image compression with EXIF handling and optimization
    
    Args:
        uploaded_file: Streamlit uploaded file
        max_size: Maximum dimensions (width, height)
        quality: JPEG quality (1-95)
    
    Returns:
        Compressed image as BytesIO
    """
    try:
        # Open and process image
        image = Image.open(uploaded_file)
        
        # Handle EXIF rotation
        try:
            image = ImageOps.exif_transpose(image)
        except Exception:
            pass  # Skip if EXIF data is corrupted
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if image.mode in ('RGBA', 'P', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            
            if image.mode in ('RGBA', 'LA'):
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)
            image = background
        
        # Calculate resize dimensions maintaining aspect ratio
        original_width, original_height = image.size
        max_width, max_height = max_size
        
        # Only resize if image is larger than max_size
        if original_width > max_width or original_height > max_height:
            ratio = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Use high-quality resampling
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save compressed image to bytes
        output = io.BytesIO()
        
        # Determine save format based on file extension
        file_ext = uploaded_file.name.split('.')[-1].lower()
        format_map = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'gif': 'GIF',
            'webp': 'WEBP'
        }
        
        save_format = format_map.get(file_ext, 'JPEG')
        
        # Optimize compression settings
        if save_format == 'JPEG':
            image.save(output, format=save_format, quality=quality, optimize=True)
        elif save_format == 'PNG':
            image.save(output, format=save_format, optimize=True, compress_level=9)
        else:
            image.save(output, format=save_format, optimize=True)
        
        output.seek(0)
        return output
        
    except Exception as e:
        st.error(f"❌ Error compressing image: {str(e)}")
        # Return original file content as fallback
        uploaded_file.seek(0)
        return io.BytesIO(uploaded_file.read())

def validate_image(uploaded_file) -> bool:
    """
    Professional image validation with detailed error reporting
    
    Args:
        uploaded_file: Streamlit uploaded file
    
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            st.error(f"❌ File size ({format_file_size(uploaded_file.size)}) exceeds the {format_file_size(max_size)} limit")
            return False
        
        # Check file type
        allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
        if uploaded_file.type not in allowed_types:
            st.error("❌ Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP files.")
            return False
        
        # Validate file extension
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in allowed_extensions:
            st.error(f"❌ Invalid file extension '{file_extension}'. Allowed: {', '.join(allowed_extensions)}")
            return False
        
        # Try to open and verify image
        try:
            image = Image.open(uploaded_file)
            image.verify()
            uploaded_file.seek(0)  # Reset file pointer after verification
            
            # Re-open for dimension check (verify() can't be used twice)
            image = Image.open(uploaded_file)
            width, height = image.size
            
            # Check image dimensions (reasonable limits)
            max_dimension = 10000
            min_dimension = 10
            
            if width > max_dimension or height > max_dimension:
                st.error(f"❌ Image dimensions ({width}x{height}) too large. Maximum: {max_dimension}x{max_dimension} pixels.")
                return False
            
            if width < min_dimension or height < min_dimension:
                st.error(f"❌ Image dimensions ({width}x{height}) too small. Minimum: {min_dimension}x{min_dimension} pixels.")
                return False
            
            # Check for corrupted images
            try:
                image.load()
            except Exception as e:
                st.error(f"❌ Image appears to be corrupted: {str(e)}")
                return False
            
            uploaded_file.seek(0)  # Reset file pointer
            return True
            
        except Exception as e:
            st.error(f"❌ Invalid image file: {str(e)}")
            return False
    
    except Exception as e:
        st.error(f"❌ Error validating file: {str(e)}")
        return False

def get_image_metadata(uploaded_file) -> dict:
    """
    Extract comprehensive image metadata
    
    Args:
        uploaded_file: Streamlit uploaded file
    
    Returns:
        Dictionary with image metadata
    """
    try:
        image = Image.open(uploaded_file)
        metadata = {
            'filename': uploaded_file.name,
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.size[0],
            'height': image.size[1],
            'file_size': uploaded_file.size,
            'file_size_formatted': format_file_size(uploaded_file.size)
        }
        
        # Extract EXIF data if available
        exif_data = {}
        if hasattr(image, '_getexif') and image._getexif() is not None:
            exif = image._getexif()
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                exif_data[tag] = value
        
        metadata['exif'] = exif_data
        
        # Calculate aspect ratio
        aspect_ratio = metadata['width'] / metadata['height']
        metadata['aspect_ratio'] = round(aspect_ratio, 2)
        
        # Determine orientation
        if metadata['width'] > metadata['height']:
            metadata['orientation'] = 'landscape'
        elif metadata['width'] < metadata['height']:
            metadata['orientation'] = 'portrait'
        else:
            metadata['orientation'] = 'square'
        
        uploaded_file.seek(0)
        return metadata
        
    except Exception as e:
        st.error(f"Error extracting metadata: {str(e)}")
        return {}

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format with precise units
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def validate_text_input(text: str, min_length: int = 1, max_length: int = 100, 
                       field_name: str = "Text") -> Tuple[bool, str]:
    """
    Professional text input validation with detailed feedback
    
    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, message)
    """
    if not text or not text.strip():
        return False, f"{field_name} cannot be empty"
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"{field_name} must be at least {min_length} characters long"
    
    if len(text) > max_length:
        return False, f"{field_name} must be less than {max_length} characters long"
    
    # Check for potentially harmful content
    if contains_harmful_content(text):
        return False, f"{field_name} contains potentially harmful content"
    
    return True, text

def contains_harmful_content(text: str) -> bool:
    """
    Basic check for potentially harmful content
    
    Args:
        text: Text to check
    
    Returns:
        True if potentially harmful content detected
    """
    # Basic list of potentially harmful patterns
    harmful_patterns = [
        r'<script.*?>.*?</script>',  # Script tags
        r'javascript:',              # JavaScript protocols
        r'data:.*?base64',          # Data URLs with base64
        r'vbscript:',               # VBScript
        r'onload\s*=',              # Event handlers
        r'onerror\s*=',
        r'onclick\s*=',
    ]
    
    text_lower = text.lower()
    for pattern in harmful_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    return False

def sanitize_filename(filename: str) -> str:
    """
    Professional filename sanitization for safe storage
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = re.sub(r'\s+', '_', filename)
    
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Remove leading/trailing underscores and dots
    filename = filename.strip('_.')
    
    # Ensure filename is not empty
    if not filename:
        filename = "untitled"
    
    # Limit length
    max_length = 100
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length-len(ext)] + ext
    
    return filename

def generate_file_hash(file_content: bytes) -> str:
    """
    Generate SHA-256 hash of file content for duplicate detection
    
    Args:
        file_content: File content as bytes
    
    Returns:
        SHA-256 hash string
    """
    return hashlib.sha256(file_content).hexdigest()

def create_thumbnail(image_path: str, thumbnail_size: Tuple[int, int] = (200, 200)) -> Optional[io.BytesIO]:
    """
    Create thumbnail from image file
    
    Args:
        image_path: Path to image file
        thumbnail_size: Thumbnail dimensions
    
    Returns:
        Thumbnail as BytesIO or None if error
    """
    try:
        with Image.open(image_path) as image:
            # Create thumbnail maintaining aspect ratio
            image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Save thumbnail
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=80, optimize=True)
            output.seek(0)
            return output
            
    except Exception as e:
        st.error(f"Error creating thumbnail: {str(e)}")
        return None

def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """
    Validate geographical coordinates
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if not (-90 <= lat <= 90):
            return False, "Latitude must be between -90 and 90 degrees"
        
        if not (-180 <= lon <= 180):
            return False, "Longitude must be between -180 and 180 degrees"
        
        return True, "Coordinates are valid"
        
    except (ValueError, TypeError):
        return False, "Coordinates must be valid numbers"

def estimate_processing_time(file_size: int) -> str:
    """
    Estimate processing time based on file size
    
    Args:
        file_size: File size in bytes
    
    Returns:
        Estimated time string
    """
    # Simple estimation based on file size
    if file_size < 1024 * 1024:  # < 1MB
        return "< 1 second"
    elif file_size < 5 * 1024 * 1024:  # < 5MB
        return "1-3 seconds"
    elif file_size < 10 * 1024 * 1024:  # < 10MB
        return "3-5 seconds"
    else:
        return "5-10 seconds"
