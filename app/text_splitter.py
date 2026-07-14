def chunk_text(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")
    
    cleaned_text = " ".join(text.split())

    if not cleaned_text:
        return []
    
    chunks: list[str] = []
    start = 0

    while start < len(cleaned_text):
        end = min(start + chunk_size, len(cleaned_text))

        if end < len(cleaned_text):
            last_space = cleaned_text.rfind(" ", start, end)

            if last_space > start:
                end = last_space

        chunk = cleaned_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(cleaned_text):
            break

        start = end - overlap

    return chunks