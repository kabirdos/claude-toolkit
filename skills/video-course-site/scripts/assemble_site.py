#!/usr/bin/env python3
"""Assemble a tabbed course site from HTML post files.

Usage:
  python3 assemble_site.py /path/to/video/folder

Expects posts in <folder>/site/posts/*.html
Outputs <folder>/site/index.html
"""
import os
import sys

def assemble(folder):
    sitedir = os.path.join(folder, "site")
    postsdir = os.path.join(sitedir, "posts")

    if not os.path.exists(postsdir):
        print(f"No posts directory found at {postsdir}")
        return

    posts = sorted(f for f in os.listdir(postsdir) if f.endswith('.html'))
    if not posts:
        print("No post files found.")
        return

    print(f"Found {len(posts)} posts")
    course_name = os.path.basename(folder)

    tab_buttons = []
    tab_divs = []
    for i, post_file in enumerate(posts):
        tab_id = post_file.replace('.html', '')
        label = tab_id.replace('-', ' ').replace('class ', 'Class ').title()
        if tab_id == 'overview':
            label = 'Overview'

        active_cls = ' class="active"' if i == 0 else ''
        active_div = ' active' if i == 0 else ''

        tab_buttons.append(f'      <button{active_cls} data-tab="{tab_id}">{label}</button>')

        with open(os.path.join(postsdir, post_file)) as f:
            content = f.read()
        tab_divs.append(f'    <div id="{tab_id}" class="tab-content{active_div}">\n{content}\n    </div>')

    buttons_html = "\n".join(tab_buttons)
    content_html = "\n".join(tab_divs)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{course_name}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: Georgia, 'Times New Roman', serif;
      font-size: 20px; line-height: 1.7; color: #292929;
      background: #fff; -webkit-font-smoothing: antialiased;
    }}
    .site-header {{
      border-bottom: 1px solid #e6e6e6; padding: 2rem 1.5rem 0; background: #fafafa;
    }}
    .site-header h1 {{
      font-family: Georgia, serif; font-size: 2.4rem; font-weight: 700;
      letter-spacing: -0.02em; color: #1a1a1a; max-width: 740px; margin: 0 auto;
    }}
    .site-header .subtitle {{
      font-family: Georgia, serif; font-size: 1.1rem; color: #757575;
      max-width: 740px; margin: 0.3rem auto 0; font-style: italic;
    }}
    .tab-nav {{
      max-width: 900px; margin: 0 auto; padding-top: 1.2rem;
      display: flex; gap: 0; overflow-x: auto;
      -webkit-overflow-scrolling: touch; scrollbar-width: none;
    }}
    .tab-nav::-webkit-scrollbar {{ display: none; }}
    .tab-nav button {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 0.82rem; font-weight: 500; color: #757575; background: none;
      border: none; border-bottom: 2px solid transparent;
      padding: 0.6rem 1rem; cursor: pointer; white-space: nowrap;
      transition: color 0.15s, border-color 0.15s;
    }}
    .tab-nav button:hover {{ color: #292929; }}
    .tab-nav button.active {{ color: #1a1a1a; border-bottom-color: #1a1a1a; }}
    .content {{ max-width: 740px; margin: 0 auto; padding: 2.5rem 1.5rem 5rem; }}
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}
    .content h2 {{
      font-family: Georgia, serif; font-size: 2rem; font-weight: 700;
      letter-spacing: -0.02em; color: #1a1a1a; margin-bottom: 0.5rem; line-height: 1.25;
    }}
    .content h3 {{
      font-family: Georgia, serif; font-size: 1.4rem; font-weight: 700;
      color: #1a1a1a; margin-top: 2.5rem; margin-bottom: 0.8rem; line-height: 1.3;
    }}
    .content p {{ margin-bottom: 1.4rem; color: #292929; }}
    .content blockquote {{
      border-left: 3px solid #e0e0e0; margin: 1.5rem 0; padding: 0.8rem 1.5rem;
      color: #555; font-style: italic; background: #fafafa; border-radius: 0 4px 4px 0;
    }}
    .content blockquote strong {{ font-style: normal; color: #333; }}
    .content blockquote p {{ margin-bottom: 0.5rem; color: inherit; }}
    .content blockquote p:last-child {{ margin-bottom: 0; }}
    .content ul, .content ol {{ margin-bottom: 1.4rem; padding-left: 1.8rem; }}
    .content li {{ margin-bottom: 0.5rem; }}
    .meditation-marker, .content div.meditation-marker {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 0.85rem; color: #8b6914; background: #fef9e7;
      border: 1px solid #f5e6b8; border-radius: 6px;
      padding: 0.5rem 1rem; margin: 1.5rem 0; display: inline-block;
    }}
    @media (max-width: 768px) {{
      body {{ font-size: 18px; }}
      .site-header h1 {{ font-size: 1.8rem; }}
      .content h2 {{ font-size: 1.6rem; }}
      .content h3 {{ font-size: 1.2rem; }}
      .tab-nav button {{ font-size: 0.75rem; padding: 0.5rem 0.7rem; }}
      .content {{ padding: 1.5rem 1rem 3rem; }}
    }}
    .site-footer {{
      border-top: 1px solid #e6e6e6; padding: 2rem 1.5rem; text-align: center;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 0.8rem; color: #999;
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <h1>{course_name}</h1>
    <nav class="tab-nav" id="tabNav">
{buttons_html}
    </nav>
  </header>
  <main class="content">
{content_html}
  </main>
  <footer class="site-footer">{course_name}</footer>
  <script>
    const tabNav = document.getElementById('tabNav');
    const tabs = tabNav.querySelectorAll('button');
    const contents = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {{
      tab.addEventListener('click', () => {{
        const target = tab.dataset.tab;
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(target).classList.add('active');
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
        history.replaceState(null, '', '#' + target);
      }});
    }});
    window.addEventListener('load', () => {{
      const hash = location.hash.slice(1);
      if (hash) {{
        const tab = tabNav.querySelector('[data-tab="' + hash + '"]');
        if (tab) tab.click();
      }}
    }});
  </script>
</body>
</html>'''

    os.makedirs(sitedir, exist_ok=True)
    output = os.path.join(sitedir, "index.html")
    with open(output, "w") as f:
        f.write(html)
    print(f"Built: {output} ({os.path.getsize(output)/1e3:.0f} KB)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 assemble_site.py /path/to/video/folder")
        sys.exit(1)
    folder = os.path.abspath(sys.argv[1])
    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a directory")
        sys.exit(1)
    assemble(folder)
