def split_message(content, char_limit=2000):
    """
    Split a long message into multiple smaller messages to fit within Discord's character limit
    
    Args:
        content (str): The message content to split
        char_limit (int): The character limit for each message (Discord's limit is 2000)
        
    Returns:
        list: A list of message chunks, each within the character limit
    """
    # If the content is already within the limit, return it as a single-item list
    if len(content) <= char_limit:
        return [content]
    
    # Split the message into chunks
    chunks = []
    current_chunk = ""
    
    # Try to split at paragraph breaks first
    paragraphs = content.split('\n\n')
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed the limit, add the current chunk to chunks
        # and start a new chunk with this paragraph
        if len(current_chunk) + len(paragraph) + 2 > char_limit:
            # If the current chunk is not empty, add it to chunks
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                # If this single paragraph is too long, split it by sentences
                sentences = paragraph.replace('. ', '.\n').split('\n')
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 > char_limit:
                        if current_chunk:
                            chunks.append(current_chunk)
                            current_chunk = sentence
                        else:
                            # If a single sentence is too long, split it by words
                            words = sentence.split(' ')
                            for word in words:
                                if len(current_chunk) + len(word) + 1 > char_limit:
                                    chunks.append(current_chunk)
                                    current_chunk = word
                                else:
                                    current_chunk += ' ' + word if current_chunk else word
                    else:
                        current_chunk += '\n' + sentence if current_chunk else sentence
        else:
            # Add paragraph separator if current_chunk is not empty
            current_chunk += '\n\n' + paragraph if current_chunk else paragraph
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
