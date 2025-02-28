import re

def markdown_to_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        md_text = file.read()
    
    md_text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', md_text)
    
    md_text = re.sub(r'(?<!!)\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', md_text)
    
    md_text = re.sub(r'^(#{1,3})\s*(.+)$', lambda m: f"<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>", md_text, flags=re.MULTILINE)
    
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', md_text)
    
    md_text = re.sub(r'(?<!\*)\*(?!\*)(.*?)\*(?!\*)', r'<i>\1</i>', md_text)
    
    def replace_list(match):
        items = match.group(0).split('\n')
        items = [re.sub(r'\d+\.\s*(.*)', r'<li>\1</li>', item) for item in items if item.strip()]
        return '<ol>\n' + '\n'.join(items) + '\n</ol>'
    
    md_text = re.sub(r'(?m)(^\d+\.\s.*(?:\n\d+\.\s.*)*)', replace_list, md_text)
    
    return md_text

file_path = 'input.md'
print(markdown_to_html(file_path))

