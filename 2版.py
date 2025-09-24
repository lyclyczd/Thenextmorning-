import datetime
import re

def escape_html(text):
    """将特殊字符转换为HTML实体，防止XSS和乱码"""
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") \
               .replace('"', "&quot;").replace("'", "&#039;")

def validate_url(url):
    """简单验证URL格式"""
    if not url:
        return False
    # 基本的URL格式检查
    url_pattern = re.compile(r'^https?://[^\s]+$')
    return bool(url_pattern.match(url))

def get_theme_color():
    """获取用户选择的主题颜色"""
    colors = {
        1: ("blue", "bg-blue-500 hover:bg-blue-600"),
        2: ("green", "bg-green-500 hover:bg-green-600"),
        3: ("purple", "bg-purple-500 hover:bg-purple-600"),
        4: ("red", "bg-red-500 hover:bg-red-600"),
        5: ("yellow", "bg-yellow-500 hover:bg-yellow-600"),
        6: ("indigo", "bg-indigo-500 hover:bg-indigo-600")
    }
    
    print("\n请选择主题颜色:")
    for key, (name, _) in colors.items():
        print(f"{key}. {name}")
    
    while True:
        try:
            choice = int(input("请输入颜色编号 (1-6): "))
            if choice in colors:
                return colors[choice]
            print("请输入有效的编号 (1-6)")
        except ValueError:
            print("请输入数字")

def collect_links():
    """收集用户输入的链接列表"""
    links = []
    print("\n请添加网站链接 (输入空名称结束)")
    
    while True:
        name = input("\n网站名称: ").strip()
        if not name:  # 空名称表示结束输入
            break
            
        while True:
            url = input("网站URL (必须以http://或https://开头): ").strip()
            if validate_url(url):
                break
            print("URL格式无效，请重新输入")
            
        links.append({"name": name, "url": url})
        print(f"已添加: {name} - {url}")
    
    return links

def generate_html(links, title, description, theme_color_name, theme_color_class):
    """生成HTML内容"""
    # 生成链接卡片HTML
    links_html = ""
    for link in links:
        links_html += f'''
        <div class="link-card bg-white rounded-lg shadow-sm p-4 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
            <h3 class="font-semibold text-gray-800 mb-1">{escape_html(link['name'])}</h3>
            <p class="text-sm text-gray-500 mb-3 truncate">{escape_html(link['url'])}</p>
            <a href="{escape_html(link['url'])}" target="_blank" class="inline-flex items-center text-white text-sm px-4 py-2 rounded {theme_color_class}">
                <i class="fa fa-external-link mr-1"></i> 访问
            </a>
        </div>
        '''
    
    # 完整HTML模板
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(title)}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <style>
        .link-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }}
        @media (max-width: 640px) {{
            .link-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
        <header class="text-center mb-10">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">{escape_html(title)}</h1>
            <p class="text-gray-600">{escape_html(description)}</p>
            
            <div class="mt-6 relative max-w-md mx-auto">
                <input type="text" id="searchInput" placeholder="搜索链接..." 
                       class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg focus:outline-none 
                              focus:ring-2 focus:ring-{theme_color_name}-500 focus:border-{theme_color_name}-500 transition-all">
                <i class="fa fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
            </div>
        </header>
        
        <main class="link-grid">
            {links_html}
        </main>
        
        <footer class="mt-12 text-center text-gray-500 text-sm">
            <p>生成于 {datetime.date.today().strftime('%Y年%m月%d日')}</p>
        </footer>
    </div>
    
    <script>
        // 搜索功能实现
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const links = document.querySelectorAll('.link-card');
            
            links.forEach(link => {{
                const linkName = link.querySelector('h3').textContent.toLowerCase();
                link.style.display = linkName.includes(searchTerm) ? 'block' : 'none';
            }});
        }});
    </script>
</body>
</html>'''
    
    return html_template

def save_html_file(html_content, filename="website_navigation.html"):
    """将HTML内容保存到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("        网站跳转HTML生成器        ")
    print("=" * 50)
    print("这个程序将帮助你创建一个带有搜索功能的网站导航页面")
    print("生成的HTML文件可以直接在浏览器中打开使用\n")
    
    # 获取页面基本信息
    title = input("请输入页面标题 (默认: '我的导航页'): ").strip() or "我的导航页"
    description = input("请输入页面描述 (默认: '常用网站导航'): ").strip() or "常用网站导航"
    
    # 获取主题颜色
    theme_color_name, theme_color_class = get_theme_color()
    
    # 收集链接
    links = collect_links()
    
    if not links:
        print("\n警告: 没有添加任何链接，生成的页面将为空")
        if input("是否继续? (y/n): ").lower() != 'y':
            print("程序已取消")
            return
    
    # 生成HTML
    print("\n正在生成HTML文件...")
    html_content = generate_html(links, title, description, theme_color_name, theme_color_class)
    
    # 保存文件
    filename = input("\n请输入保存的文件名 (默认: website_navigation.html): ").strip() or "website_navigation.html"
    if not filename.endswith(".html"):
        filename += ".html"
    
    if save_html_file(html_content, filename):
        print(f"\n成功! HTML文件已保存为: {filename}")
        print("你可以双击该文件在浏览器中打开使用")
    else:
        print("\n生成失败，请重试")

if __name__ == "__main__":
    main()
