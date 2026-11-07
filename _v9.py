# -*- coding: utf-8 -*-
"""v9: 全站换新 LOGO 图片(1:1) + favicon + 页脚品牌区重构 + 联系方式列精简"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

SVG_RE = re.compile(r'<svg class="brand__mark" viewBox="0 0 44 54" fill="none" aria-hidden="true">.*?</svg>', re.S)

FOOTER_BRAND_RE = re.compile(
    r'<div class="footer-brand">\s*<a class="brand" href="(?:\.\./)?index\.html">.*?</a>\s*<p>.*?</p>\s*</div>', re.S)

CONTACT_UL_RE = re.compile(r'\s*<ul class="footer-contact">.*?</ul>', re.S)

n_head = n_foot = n_contact = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".git", "assets")]
    for fn in files:
        if not fn.endswith(".html"):
            continue
        p = os.path.join(root, fn)
        with open(p, encoding="utf-8") as f:
            s = f.read()
        in_article = "/article" in p.replace("\\", "/")
        pre = "../" if in_article else ""
        orig = s

        # 1) 页头/页脚 SVG -> 图片 LOGO（1:1）
        s, c = SVG_RE.subn(lambda m: '<img class="brand__mark" src="' + pre + 'assets/img/logo.png" alt="湾区（广东）数字经济研究院">', s)
        n_head += c

        # 2) 页脚品牌区：上 LOGO、中中英文名称、下简介文字
        new_brand = (
            '<div class="footer-brand">\n'
            '          <img class="footer-logo" src="' + pre + 'assets/img/logo.png" alt="湾区（广东）数字经济研究院">\n'
            '          <div class="footer-brand__name">湾区（广东）数字经济研究院</div>\n'
            '          <div class="footer-brand__sub">BAY AREA DIGITAL ECONOMY ACADEMY (GUANGDONG)</div>\n'
            '          <p>立足粤港澳大湾区，围绕数字经济、产业学院、跨境电商、人工智能、国际教育五大板块，为政府、高校与企业提供智库研究与产教融合服务。</p>\n'
            '        </div>')
        s, c2 = FOOTER_BRAND_RE.subn(lambda m: new_brand, s)
        n_foot += c2

        # 3) 联系方式列删除电话/邮箱/地址列表（保留二维码）
        s, c3 = CONTACT_UL_RE.subn('', s)
        n_contact += c3

        # 4) favicon
        if '<link rel="icon"' not in s:
            fav = ('  <link rel="icon" type="image/png" sizes="192x192" href="' + pre + 'assets/img/favicon-192.png">\n'
                   '  <link rel="shortcut icon" href="/favicon.ico">\n'
                   '  <link rel="apple-touch-icon" href="' + pre + 'assets/img/favicon-192.png">\n')
            s = s.replace('  <link rel="stylesheet" href="' + pre + 'assets/css/style.css">',
                          fav + '  <link rel="stylesheet" href="' + pre + 'assets/css/style.css">', 1)

        if s != orig:
            with open(p, "w", encoding="utf-8") as f:
                f.write(s)

print("logo img replaced:", n_head)
print("footer-brand rebuilt:", n_foot)
print("contact ul removed:", n_contact)
