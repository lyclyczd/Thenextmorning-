import os
import datetime

def get_user_input():
    """获取用户输入的网站标题和链接列表"""
    print("=== HTML链接生成器 ===")
    site_title = input("请输入网站标题（默认：我的导航网站）：").strip()
    if not site_title:
        site_title = "我的导航网站"
    
    links = []
    print("\n请输入链接信息（输入空名称结束）")
    while True:
        name = input("链接名称：").strip()
        if not name:
            break
            
        url = input("链接地址：").strip()
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        links.append({"name": name, "url": url})
        print(f"已添加：{name} -> {url}\n")
    
    if not links:
        print("警告：没有添加任何链接，将使用示例链接")
        links = [
            {"name": "百度", "url": "https://www.baidu.com"},
            {"name": "谷歌", "url": "https://www.google.com"},
            {"name": "GitHub", "url": "https://github.com"}
        ]
    
    return site_title, links

def generate_html(site_title, links):
    """生成HTML内容"""
    # 生成链接列表HTML
    links_html = ""
    for link in links:
        links_html += f"""
        <a href="{link['url']}" class="link-item group" target="_blank">
            <div class="flex items-center p-4 rounded-lg bg-white shadow-sm hover:shadow-md transition-all duration-300 transform group-hover:-translate-y-1">
                <i class="fa fa-external-link text-primary mr-3 group-hover:rotate-12 transition-transform duration-300"></i>
                <span>{link['name']}</span>
            </div>
        </a>
        """
    
    # 主HTML模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#3B82F6',
                        secondary: '#10B981',
                    }}
                }}
            }}
        }}
    </script>
    <style type="text/tailwindcss">
        @layer utilities {{
            .content-auto {{
                content-visibility: auto;
            }}
            .gradient-bg {{
                background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%);
            }}
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen font-sans">
    <div class="container mx-auto px-4 py-8 max-w-5xl">
        <!-- 标题区域 -->
        <header class="text-center mb-10">
            <h1 class="text-4xl font-bold mb-3 text-gray-800">{site_title}</h1>
            <p class="text-gray-600">快速访问常用网站</p>
        </header>
        
        <!-- 搜索区域 -->
        <div class="mb-10">
            <form class="max-w-2xl mx-auto" onsubmit="window.open('https://www.google.com/search?q=' + encodeURIComponent(document.getElementById('searchInput').value), '_blank'); return false;">
                <div class="relative">
                    <input type="text" id="searchInput" 
                        placeholder="搜索..." 
                        class="w-full px-5 py-3 rounded-full border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary outline-none shadow-sm transition-all">
                    <button type="submit" class="absolute right-3 top-1/2 transform -translate-y-1/2 bg-primary text-white p-2 rounded-full hover:bg-primary/90 transition-colors">
                        <i class="fa fa-search"></i>
                    </button>
                </div>
            </form>
        </div>
        
        <!-- 链接区域 -->
        <div class="links-container grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {links_html}
        </div>
    </div>
    
    <footer class="mt-16 py-6 border-t border-gray-200 text-center text-gray-500 text-sm">
        <p>生成于 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | 由 Python HTML生成器 创建</p>
    </footer>
</body>
</html>"""
    
    return html_template

def save_html(html_content, filename=None):
    """保存HTML内容到文件"""
    if not filename:
        filename = "link_page.html"
    
    # 检查文件是否已存在
    counter = 1
    base_filename = filename
    while os.path.exists(filename):
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{counter}{ext}"
        counter += 1
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def main():
    """主函数"""
    # 获取用户输入
    site_title, links = get_user_input()
    
    # 生成HTML内容
    print("\n正在生成HTML文件...")
    html_content = generate_html(site_title, links)
    
    # 保存HTML文件
    filename = save_html(html_content)
    
    # 显示结果
    print(f"\n成功生成HTML文件：{os.path.abspath(filename)}")
    print("您可以用浏览器打开该文件查看效果")

if __name__ == "__main__":
    main()
    