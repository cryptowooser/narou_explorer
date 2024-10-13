from django import template
import re

register = template.Library()

@register.filter
def format_novel_text(value):
    # Define punctuation pairs we don't want to split
    no_split_pairs = r'[！？]?[！？』」]'
    
    # Split the text into segments that are either within quotes 「」 or outside quotes
    segments = re.split(r'(「[^」]*」)', value)
    
    formatted_segments = []
    for segment in segments:
        if segment.startswith('「') and segment.endswith('」'):
            # If it's a quoted segment, keep it as is
            formatted_segments.append(segment)
        else:
            # For non-quoted segments, apply the splitting logic
            parts = []
            last_split = 0
            for match in re.finditer(f'({no_split_pairs}|[。！？])', segment):
                if match.start() - last_split >= 20:
                    # Check if this punctuation is part of a pair we don't want to split
                    if re.match(no_split_pairs, segment[match.start():match.end()+1]):
                        continue
                    parts.append(segment[last_split:match.end()])
                    last_split = match.end()
            if last_split < len(segment):
                parts.append(segment[last_split:])
            
            formatted = '\n'.join(parts)
            formatted_segments.append(formatted)
    
    # Join all segments
    formatted = ''.join(formatted_segments)
    
    # Remove any double newlines that might have been created
    formatted = re.sub(r'\n\s*\n', '\n', formatted)
    
    return formatted
