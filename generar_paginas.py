#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de páginas HTML individuales para cada noticia
Lee noticias.json y crea un archivo HTML por cada noticia
Incluye funcionalidad de archivo de noticias antiguas
Autor: Trickzz.sh
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

# Plantilla HTML para cada noticia
PLANTILLA_NOTICIA = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="../IMG/footer.png">
    <title>{titulo} - RED</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --brand-negro: #000000;
            --brand-rojo: #cc1a1a;
            --brand-rojo-oscuro: #8b0000;
            --brand-gris: #999999;
            --brand-dark: #000000;
            --text-grey: #333333;
            --light-grey: #f4f4f4;
            --border-color: #e5e5e5;
            --bg-color: #ffffff;
            --serif-font: 'Playfair Display', Georgia, serif;
            --sans-font: 'Roboto', Helvetica, Arial, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--sans-font);
            background-color: var(--bg-color);
            color: var(--text-grey);
            line-height: 1.5;
        }}

        a {{
            text-decoration: none;
            color: inherit;
            transition: color 0.2s;
        }}

        a:hover {{
            color: var(--brand-rojo);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* HEADER */
        .header-main {{
            padding: 25px 0;
            text-align: center;
            position: relative;
        }}

        .header-main::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(to right, var(--brand-rojo) 0%, var(--brand-rojo-oscuro) 50%, var(--brand-gris) 100%);
        }}

        /* LOGO SVG - Adaptado y ampliado */
        .logo-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 30px; margin-bottom: 50px;
            
            height: 45px;
        }}

        .logo-img {{
            width: 120px;
            height: auto;
            object-fit: contain;
            object-position: center center;
            display: block;
            
        }}

        .logo-text {{
            font-size: 72px;
            font-weight: 900;
            letter-spacing: -2px;
            line-height: 1;
            font-family: var(--sans-font);
        }}

        .logo-red {{
            color: var(--brand-rojo);
        }}

        .logo-noticias {{
            color: var(--brand-negro);
        }}

        .collaboration-line {{
            font-size: 12px;
            color: #555;
            text-align: center;
            margin-top: 8px;
            margin-bottom: 5px;
            font-style: italic;
        }}

        .date-line {{
            font-size: 13px;
            color: #666;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid var(--border-color);
            display: inline-block;
            padding-left: 20px;
            padding-right: 20px;
        }}


        /* ARTÍCULO */
        .article-layout {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 40px;
            margin-top: 30px;
        }}

        .full-article-header {{
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}

        .breadcrumbs {{
            font-size: 12px;
            text-transform: uppercase;
            color: var(--brand-rojo);
            font-weight: bold;
            margin-bottom: 15px;
            display: block;
        }}

        .full-headline {{
            font-family: var(--sans-font);
            font-size: 46px;
            line-height: 1.1;
            color: var(--brand-dark);
            margin-bottom: 20px;
        }}

        .full-lead {{
            font-family: var(--sans-font);
            font-size: 20px;
            line-height: 1.5;
            color: #444;
            margin-bottom: 20px;
        }}

        .full-meta {{
            font-size: 13px;
            color: #666;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .full-image-container {{
            margin-bottom: 30px;
        }}

        .full-image-container img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .full-image-caption {{
            font-size: 13px;
            color: #777;
            background: #f9f9f9;
            padding: 8px 15px;
            border-bottom: 1px solid #eee;
        }}

        .article-body {{
            font-family: var(--sans-font);
            font-size: 19px;
            line-height: 1.8;
            color: #222;
        }}

        .article-body p {{
            margin-bottom: 25px;
        }}
        
        .article-body h2 {{
            font-family: var(--sans-font);
            font-size: 24px;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 20px;
            color: var(--brand-dark);
        }}

        .article-body ul {{
            margin-left: 30px;
            margin-bottom: 25px;
        }}

        .article-body li {{
            margin-top: 30px; margin-bottom: 50px;
        }}

        .article-quote {{
            border-left: 4px solid var(--brand-rojo);
            padding-left: 25px;
            font-style: italic;
            font-size: 24px;
            color: #444;
            margin: 40px 0;
        }}

        .btn-back {{
            display: inline-block;
            margin-bottom: 20px;
            font-size: 12px;
            font-weight: bold;
            color: #666;
            cursor: pointer;
        }}
        .btn-back:hover {{
            color: var(--brand-rojo);
            text-decoration: underline;
        }}

        .sidebar-title {{
            font-size: 14px;
            font-weight: 900;
            text-transform: uppercase;
            border-bottom: 2px solid var(--brand-dark);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}


        .related-item {{
            margin-bottom: 20px;
            border-bottom: 1px dotted #ccc;
            padding-bottom: 15px;
        }}

        .related-category {{
            font-size: 11px;
            text-transform: uppercase;
            color: var(--brand-rojo);
            font-weight: bold;
        }}

        .related-item h4 {{
            font-family: var(--sans-font);
            font-size: 16px;
            margin-top: 5px;
        }}

        .newsletter-cta {{
            display: inline-block;
            margin-top: 16px;
            font-weight: 900;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            font-size: 12px;
            color: var(--brand-rojo);
            text-decoration: none;
            border-bottom: 2px solid rgba(204, 26, 26, 0.35);
            padding-bottom: 2px;
            transition: all 0.2s ease;
        }}

        .newsletter-cta:hover {{
            border-bottom-color: var(--brand-rojo);
            filter: brightness(0.95);
        }}

        .newsletter-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.55);
            -webkit-backdrop-filter: blur(4px);
            backdrop-filter: blur(4px);
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
            z-index: 9999;
        }}

        body.newsletter-open #newsletter-modal,
        body.desuscribir-open #desuscribir-modal {{
            display: flex;
            animation: newsletterFadeIn 220ms ease-out;
        }}

        .newsletter-modal {{
            width: 100%;
            max-width: 520px;
            background: #fff;
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: 0 18px 55px rgba(0, 0, 0, 0.25);
            transform: translateY(-8px);
            opacity: 0;
            position: relative;
        }}

        .newsletter-icon {{
            width: 90px;
            height: 90px;
            border-radius: 999px;
            background: #f3f3f3;
            display: grid;
            place-items: center;
            margin: 18px auto 0 auto;
        }}

        .newsletter-icon svg {{
            width: 34px;
            height: 34px;
            color: #111;
        }}

        body.newsletter-open .newsletter-modal,
        body.desuscribir-open .newsletter-modal {{
            animation: newsletterSlideDown 260ms cubic-bezier(0.2, 0.9, 0.2, 1) forwards;
        }}

        @keyframes newsletterFadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes newsletterSlideDown {{
            from {{ transform: translateY(-14px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}

        .newsletter-modal-header {{
            padding: 14px 18px 10px 18px;
            border-bottom: 0;
            text-align: center;
            color: var(--text-grey);
        }}

        .newsletter-modal-title {{
            font-family: var(--sans-font);
            font-size: 26px;
            font-weight: 900;
            letter-spacing: -0.6px;
            color: var(--brand-dark);
        }}

        .newsletter-modal-subtitle {{
            margin-top: 4px;
            font-size: 15px;
            color: #666;
            line-height: 1.5;
        }}

        .newsletter-close {{
            position: absolute;
            top: 8px;
            right: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border: none;
            background: transparent;
            font-weight: 900;
            color: #222;
            cursor: pointer;
        }}

        .newsletter-close:hover {{
            color: var(--brand-rojo);
        }}

        .newsletter-modal-body {{
            padding: 6px 18px 18px 18px;
            color: var(--text-grey);
        }}

        .newsletter-field {{
            display: grid;
            gap: 10px;
            margin-top: 8px;
            margin-bottom: 14px;
        }}

        .newsletter-input {{
            width: 100%;
            border: 2px solid #d8d8d8;
            border-radius: 12px;
            padding: 13px 14px;
            font-size: 14px;
            outline: none;
        }}

        .newsletter-input:focus {{
            border-color: var(--brand-rojo);
            box-shadow: 0 0 0 4px rgba(204, 26, 26, 0.12);
        }}

        .newsletter-submit {{
            width: 100%;
            border: none;
            border-radius: 12px;
            padding: 13px 14px;
            background: var(--brand-rojo);
            color: #fff;
            font-weight: 900;
            letter-spacing: 0.2px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}

        .newsletter-submit:hover {{
            filter: brightness(0.95);
        }}

        .newsletter-submit:disabled {{
            opacity: 0.75;
            cursor: not-allowed;
        }}

        .newsletter-spinner {{
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255,255,255,0.4);
            border-top-color: #fff;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            display: none;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        .newsletter-note {{
            margin-top: 10px;
            font-size: 12px;
            color: #666;
            line-height: 1.45;
            text-align: center;
        }}

        /* FOOTER */
        footer {{
            background-color: #000000;
            color: #ffffff;
            padding: 20px 0;
            margin-top: 50px;
            text-align: center;
            border-top: 1px solid var(--brand-rojo-oscuro);
        }}

        .footer-grid {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: flex-start;
            gap: 40px;
        }}

        .footer-left {{
            flex: 1 1 260px;
            max-width: 360px;
            text-align: left;
        }}

        .footer-logo {{
            display: flex;
            justify-content: flex-start;
            align-items: center;
            padding: 10px 0;
            margin-bottom: 10px;
        }}

        .logo-img-footer {{
            width: auto;
            height: 56px;
            object-fit: contain;
            display: block;
        }}

        .footer-description {{
            font-size: 14px;
            color: #b0b0b0;
            line-height: 1.6;
            margin-bottom: 16px;
        }}

        .footer-copy {{
            font-size: 12px;
            color: #777777;
        }}

        .footer-col {{
            flex: 1 1 220px;
            text-align: left;
        }}

        .footer-heading {{
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: var(--brand-rojo);
            margin-bottom: 10px;
        }}

        .footer-item {{
            font-size: 13px;
            color: #d0d0d0;
            margin-bottom: 6px;
        }}

        @media (max-width: 1024px) {{
            .article-layout {{
                grid-template-columns: 1fr;
            }}
            .article-sidebar {{
                display: none;
            }}
        }}

        @media (max-width: 768px) {{
            .full-headline {{
                font-size: 32px;
            }}
            .article-sidebar {{
                display: block;
                margin-top: 40px;
            }}

            /* Logo más pequeño en móvil */
            .logo-container {{
                height: 40px;
            }}

            .logo-img {{
                width: 90px;
                transform: scale(1.0);
            }}

            .footer-logo {{
                padding: 8px 0;
            }}

            .logo-img-footer {{
                height: 40px;
            }}
        }}
    </style>
</head>
<body>

    <!-- HEADER LOGO -->
    <header class="header-main">
        <div class="container">
            <a href="../index.html" class="logo-container">
                <img src="../IMG/footer.png" alt="RED" class="logo-img">
            </a>
            <div class="collaboration-line">
                En colaboración con <strong>Diario El Mundo</strong>
            </div>
            <div class="date-line">
                {fecha_actualizacion}
            </div>
        </div>
    </header>

    <!-- CONTENIDO ARTÍCULO -->
    <main class="container">
        <a href="../index.html" class="btn-back">&larr; VOLVER A PORTADA</a>
        
        <div class="article-layout">
            <!-- CONTENIDO PRINCIPAL -->
            <div class="article-content">
                <header class="full-article-header">
                    <span class="breadcrumbs">{categoria}</span>
                    <h1 class="full-headline">{titulo}</h1>
                    <p class="full-lead">{lead}</p>
                    <div class="full-meta">
                        <span>{autor_completo}</span>
                        <span>{fecha_actualizacion}</span>
                    </div>
                </header>

                {imagen_html}

                <div class="article-body">
                    {contenido_html}
                </div>
            </div>

            <!-- SIDEBAR -->
            <aside class="article-sidebar">
                <div class="sidebar-title">Noticias Relacionadas</div>
                <div class="related-item">
                    <div class="related-category">Contexto</div>
                    <h4><a href="../index.html">Volver a la portada</a></h4>
                </div>
            </aside>
        </div>
    </main>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-left">
                    <div class="footer-logo">
                        <img src="../IMG/footer.png" alt="RED" class="logo-img-footer">
                    </div>
                    <p class="footer-description">
                        Conectando negocios con inteligencia operativa. Más de 20 años liderando la comunicación crítica en Centroamérica.
                    </p>
                    <p class="footer-copy">
                        © 2026 RED INTELFON.
                    </p>
                </div>

                <div class="footer-col">
                    <h4 class="footer-heading">EL SALVADOR</h4>
                    <p class="footer-item">
                        Urbanización Industrial Santa Elena, Calle Siemens #67 Antiguo Cuscatlán.
                    </p>
                    <p class="footer-item">
                        Tel: +503 2515 0000
                    </p>
                    <p class="footer-item">
                        Email: negocios@red.com.sv
                    </p>
                    <p class="footer-item">
                        WhatsApp: +503 7984-0006
                    </p>
                </div>

                <div class="footer-col">
                    <h4 class="footer-heading">GUATEMALA</h4>
                    <p class="footer-item">
                        TEC III, Campus Tecnológico TEC III, nivel 7, Oficina 702, Vía 3 1-01, Ciudad de Guatemala.
                    </p>
                    <p class="footer-item">
                        Tel: +502 2375 1414
                    </p>
                    <p class="footer-item">
                        Email: negocios@red.com.gt
                    </p>
                    <p class="footer-item">
                        WhatsApp: +502 3603-1010
                    </p>
                </div>
            </div>
            <div style="display:flex; gap:32px; flex-wrap:wrap; align-items:center;">
                <a class="newsletter-cta" href="#" data-newsletter-open="1">Suscribirse al newsletter</a>
                <a class="newsletter-cta" href="#" data-desuscribir-open="1" style="color:#666; border-bottom-color:rgba(100,100,100,0.35);">Desuscribirse</a>
            </div>
        </div>
    </footer>

    <div id="desuscribir-modal" class="newsletter-overlay" aria-hidden="true">
        <div class="newsletter-modal" role="dialog" aria-modal="true" aria-label="Desuscripción del newsletter">
            <div class="newsletter-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 7.5C4 6.67157 4.67157 6 5.5 6H18.5C19.3284 6 20 6.67157 20 7.5V16.5C20 17.3284 19.3284 18 18.5 18H5.5C4.67157 18 4 17.3284 4 16.5V7.5Z" stroke="currentColor" stroke-width="1.8"/>
                    <path d="M6 8.5L12 12.5L18 8.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div class="newsletter-modal-header">
                <div>
                    <div class="newsletter-modal-title">Cancelar suscripción</div>
                    <div class="newsletter-modal-subtitle">Ingresa tu correo para desuscribirte.</div>
                </div>
                <button class="newsletter-close" id="desuscribir-close" type="button" aria-label="Cerrar">✕</button>
            </div>
            <div class="newsletter-modal-body">
                <form id="desuscribir-form">
                    <div class="newsletter-field">
                        <input class="newsletter-input" id="desuscribir-correo" name="correo" type="email" placeholder="tu@correo.com" required>
                    </div>
                    <button class="newsletter-submit" type="submit">
                        <span class="newsletter-spinner" id="desuscribir-spinner"></span>
                        <span id="desuscribir-btn-text">Desuscribirme →</span>
                    </button>
                    <div class="newsletter-note">
                        Lamentamos verte ir. Puedes volver cuando quieras.
                    </div>
                </form>
                <div id="desuscribir-ok" style="display:none; text-align:center; padding: 20px 0; font-size:15px; color:#333;">
                    ¡Te has desuscrito correctamente!
                </div>
            </div>
        </div>
    </div>

    <div id="newsletter-modal" class="newsletter-overlay" aria-hidden="true">
        <div class="newsletter-modal" role="dialog" aria-modal="true" aria-label="Suscripción al newsletter">
            <div class="newsletter-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 7.5C4 6.67157 4.67157 6 5.5 6H18.5C19.3284 6 20 6.67157 20 7.5V16.5C20 17.3284 19.3284 18 18.5 18H5.5C4.67157 18 4 17.3284 4 16.5V7.5Z" stroke="currentColor" stroke-width="1.8"/>
                    <path d="M6 8.5L12 12.5L18 8.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div class="newsletter-modal-header">
                <div>
                    <div class="newsletter-modal-title">Mantente informado</div>
                    <div class="newsletter-modal-subtitle">Recibe un resumen diario en tu correo.</div>
                </div>
                <button class="newsletter-close" type="button" aria-label="Cerrar">✕</button>
            </div>
            <div class="newsletter-modal-body">
                <form id="newsletter-form">
                    <div class="newsletter-field">
                        <input class="newsletter-input" id="newsletter-correo" name="correo" type="email" placeholder="tu@correo.com" required>
                    </div>
                    <button class="newsletter-submit" type="submit">
                        <span class="newsletter-spinner" id="newsletter-spinner"></span>
                        <span id="newsletter-btn-text">Suscribirme →</span>
                    </button>
                    <div class="newsletter-note">
                        Sin spam. Cancela cuando quieras.
                    </div>
                </form>
                <div id="newsletter-ok" style="display:none; text-align:center; padding: 20px 0; font-size:15px; color:#333;">
                    ¡Te has suscrito correctamente!
                </div>
            </div>
        </div>
    </div>

    <script>
        (function () {{
            const body = document.body;
            const overlay = document.getElementById('newsletter-modal');
            const closeBtn = document.querySelector('.newsletter-close');
            const input = document.getElementById('newsletter-correo');
            const openLinks = document.querySelectorAll('[data-newsletter-open="1"]');

            function openNewsletter() {{
                body.classList.add('newsletter-open');
                if (overlay) overlay.setAttribute('aria-hidden', 'false');
                if (input) setTimeout(() => input.focus(), 50);
            }}

            function closeNewsletter() {{
                body.classList.remove('newsletter-open');
                if (overlay) overlay.setAttribute('aria-hidden', 'true');
            }}

            openLinks.forEach((a) => {{
                a.addEventListener('click', (e) => {{
                    e.preventDefault();
                    openNewsletter();
                }});
            }});

            if (closeBtn) closeBtn.addEventListener('click', closeNewsletter);
            if (overlay) {{
                overlay.addEventListener('click', (e) => {{
                    if (e.target === overlay) closeNewsletter();
                }});
            }}

            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') closeNewsletter();
            }});

            const form = document.getElementById('newsletter-form');
            const okMsg = document.getElementById('newsletter-ok');
            if (form) {{
                let enviando = false;
                form.addEventListener('submit', async (e) => {{
                    e.preventDefault();
                    if (enviando) return;
                    enviando = true;
                    const btn = form.querySelector('.newsletter-submit');
                    if (btn) {{
                        btn.disabled = true;
                        const txt = document.getElementById('newsletter-btn-text');
                        const spinner = document.getElementById('newsletter-spinner');
                        if (txt) txt.textContent = 'Enviando...';
                        if (spinner) spinner.style.display = 'inline-block';
                    }}
                    const correo = document.getElementById('newsletter-correo').value.trim();
                    if (!correo || !correo.includes('@')) {{
                        enviando = false;
                        if (btn) btn.disabled = false;
                        const txt = document.getElementById('newsletter-btn-text');
                        const spinner = document.getElementById('newsletter-spinner');
                        if (txt) txt.textContent = 'Suscribirme →';
                        if (spinner) spinner.style.display = 'none';
                        return;
                    }}
                    let resp = null;
                    try {{
                        resp = await fetch('https://hook.eu2.make.com/l7urtkvoaebrukf3jeimpaoulln2ds81', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{
                                accion: 'suscripcion',
                                correo: correo,
                                email: correo,
                                input: correo,
                                origen: 'web'
                            }})
                        }});
                        if (!resp.ok) throw new Error('Error enviando suscripción');
                    }} catch (_) {{}}
                    if (resp && resp.ok) {{
                        form.style.display = 'none';
                        if (okMsg) okMsg.style.display = 'block';
                    }} else {{
                        enviando = false;
                        if (btn) btn.disabled = false;
                        const txt = document.getElementById('newsletter-btn-text');
                        const spinner = document.getElementById('newsletter-spinner');
                        if (txt) txt.textContent = 'Suscribirme →';
                        if (spinner) spinner.style.display = 'none';
                        alert('No se pudo completar la suscripción. Intenta de nuevo.');
                    }}
                }});
            }}
        }})();

        (function () {{
            const body = document.body;
            const overlay = document.getElementById('desuscribir-modal');
            const closeBtn = document.getElementById('desuscribir-close');
            const input = document.getElementById('desuscribir-correo');
            const openLinks = document.querySelectorAll('[data-desuscribir-open="1"]');

            function openModal() {{
                body.classList.add('desuscribir-open');
                if (overlay) overlay.setAttribute('aria-hidden', 'false');
                if (input) setTimeout(() => input.focus(), 50);
            }}

            function closeModal() {{
                body.classList.remove('desuscribir-open');
                if (overlay) overlay.setAttribute('aria-hidden', 'true');
            }}

            openLinks.forEach((a) => {{
                a.addEventListener('click', (e) => {{
                    e.preventDefault();
                    openModal();
                }});
            }});

            if (closeBtn) closeBtn.addEventListener('click', closeModal);
            if (overlay) {{
                overlay.addEventListener('click', (e) => {{
                    if (e.target === overlay) closeModal();
                }});
            }}

            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') closeModal();
            }});

            const form = document.getElementById('desuscribir-form');
            const okMsg = document.getElementById('desuscribir-ok');
            if (form) {{
                let enviando = false;
                form.addEventListener('submit', async (e) => {{
                    e.preventDefault();
                    if (enviando) return;
                    enviando = true;
                    const btn = form.querySelector('.newsletter-submit');
                    if (btn) {{
                        btn.disabled = true;
                        const txt = document.getElementById('desuscribir-btn-text');
                        const spinner = document.getElementById('desuscribir-spinner');
                        if (txt) txt.textContent = 'Enviando...';
                        if (spinner) spinner.style.display = 'inline-block';
                    }}
                    const correo = document.getElementById('desuscribir-correo').value.trim();
                    if (!correo || !correo.includes('@')) {{
                        enviando = false;
                        if (btn) btn.disabled = false;
                        const txt = document.getElementById('desuscribir-btn-text');
                        const spinner = document.getElementById('desuscribir-spinner');
                        if (txt) txt.textContent = 'Desuscribirme →';
                        if (spinner) spinner.style.display = 'none';
                        return;
                    }}
                    let resp = null;
                    try {{
                        resp = await fetch('https://hook.eu2.make.com/l7urtkvoaebrukf3jeimpaoulln2ds81', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{
                                accion: 'desuscripcion',
                                correo: correo,
                                email: correo,
                                input: correo,
                                origen: 'web'
                            }})
                        }});
                        if (!resp.ok) throw new Error('Error enviando desuscripción');
                    }} catch (_) {{}}
                    if (resp && resp.ok) {{
                        form.style.display = 'none';
                        if (okMsg) okMsg.style.display = 'block';
                    }} else {{
                        enviando = false;
                        if (btn) btn.disabled = false;
                        const txt = document.getElementById('desuscribir-btn-text');
                        const spinner = document.getElementById('desuscribir-spinner');
                        if (txt) txt.textContent = 'Desuscribirme →';
                        if (spinner) spinner.style.display = 'none';
                        alert('No se pudo completar la desuscripción. Intenta de nuevo.');
                    }}
                }});
            }}
        }})();
    </script>

    </body>
    </html>
"""


# Plantilla simple para páginas de redirección cuando una noticia
# se ha movido a la carpeta de archivo `noticias_ant/`
PLANTILLA_REDIRECCION = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/png" href="../IMG/footer.png">
    <title>RED - Archivo</title>
    <meta http-equiv="refresh" content="0; url=../noticias_ant/{archivo}">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #fafafa;
            color: #333;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }}
        .card {{
            background: #fff;
            padding: 24px 28px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            max-width: 480px;
            text-align: center;
        }}
        h1 {{
            font-size: 20px;
            margin-top: 30px; margin-bottom: 50px;
        }}
        p {{
            font-size: 14px;
            margin-bottom: 16px;
        }}
        a {{
            color: var(--brand-rojo);
            text-decoration: none;
            font-weight: 600;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Esta noticia ha sido archivada</h1>
        <p>Estás siendo redirigido a la versión archivada de este artículo.</p>
        <p>Si la redirección no ocurre automáticamente, haz clic en el siguiente enlace:</p>
        <p><a href="../noticias_ant/{archivo}">Ver noticia archivada</a></p>
    </div>
</body>
</html>
"""


def generar_contenido_html(noticia):
    """Genera el HTML del contenido de la noticia"""
    html = ""
    
    # Añadir párrafos
    for parrafo in noticia.get('contenido_completo', []):
        html += f"<p>{parrafo}</p>\n"
    
    # Añadir cita si existe
    if noticia.get('citas') and len(noticia['citas']) > 0:
        html += f'<blockquote class="article-quote">"{noticia["citas"][0]}"</blockquote>\n'
    
    # Añadir puntos clave
    if noticia.get('puntos_clave') and len(noticia['puntos_clave']) > 0:
        html += '<h2>Puntos clave</h2>\n<ul>\n'
        for punto in noticia['puntos_clave']:
            html += f'<li>{punto}</li>\n'
        html += '</ul>\n'
    
    return html


def generar_autor_completo(noticia):
    """Genera el texto completo del autor"""
    autor = f"Por <strong>{noticia['autor']}</strong>"
    if noticia.get('coautor'):
        autor += f" y <strong>{noticia['coautor']}</strong>"
    autor += f" | {noticia.get('ciudad', 'Madrid')}"
    return autor


def generar_imagen_html(noticia):
    """Genera el HTML de la imagen si existe"""
    if noticia.get('imagen'):
        return f"""<div class="full-image-container">
                    <img src="{noticia['imagen']}" alt="{noticia.get('imagen_alt', '')}">
                    <div class="full-image-caption">{noticia.get('imagen_caption', '')}</div>
                </div>"""
    return ""


def generar_lead(noticia):
    """Genera el lead de la noticia"""
    if noticia.get('resumen'):
        return noticia['resumen']
    elif noticia.get('contenido_completo') and len(noticia['contenido_completo']) > 0:
        # Extraer texto del primer párrafo sin etiquetas HTML
        primer_parrafo = noticia['contenido_completo'][0]
        # Quitar etiquetas HTML básicas
        texto_limpio = primer_parrafo.replace('<strong>', '').replace('</strong>', '')
        texto_limpio = texto_limpio.replace('<em>', '').replace('</em>', '')
        return texto_limpio[:200] + '...'
    return ""


def generar_pagina_noticia(noticia, config):
    """Genera una página HTML individual para una noticia"""
    contenido_html = generar_contenido_html(noticia)
    autor_completo = generar_autor_completo(noticia)
    imagen_html = generar_imagen_html(noticia)
    lead = generar_lead(noticia)
    
    html = PLANTILLA_NOTICIA.format(
        titulo=noticia['titulo'],
        categoria=noticia['categoria'],
        lead=lead,
        autor_completo=autor_completo,
        fecha_actualizacion=config['fecha_actualizacion'],
        imagen_html=imagen_html,
        contenido_html=contenido_html
    )
    
    return html


def guardar_noticias_en_historial(noticias_actuales_json):
    """
    Guarda las noticias actuales en el historial completo
    Este historial se usa luego para el archivo
    """
    archivo_historial = 'historial_completo.json'
    historial = {}
    
    # Cargar historial existente
    if Path(archivo_historial).exists():
        try:
            with open(archivo_historial, 'r', encoding='utf-8') as f:
                historial = json.load(f)
        except:
            historial = {}
    
    # Recopilar todas las noticias actuales
    todas_noticias = []
    if 'noticia_principal' in noticias_actuales_json:
        todas_noticias.append(noticias_actuales_json['noticia_principal'])
    if 'noticias_secundarias' in noticias_actuales_json:
        todas_noticias.extend(noticias_actuales_json['noticias_secundarias'])
    if 'noticias_lo_ultimo' in noticias_actuales_json:
        todas_noticias.extend(noticias_actuales_json['noticias_lo_ultimo'])
    
    # Agregar al historial (clave: id, valor: datos completos de la noticia)
    for noticia in todas_noticias:
        if 'id' in noticia:
            # Agregar fecha de primera publicación si no existe
            if noticia['id'] not in historial:
                noticia_copia = noticia.copy()
                noticia_copia['fecha_primera_publicacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                historial[noticia['id']] = noticia_copia
    
    # Guardar historial actualizado
    with open(archivo_historial, 'w', encoding='utf-8') as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)


def archivar_noticias_antiguas(noticias_actuales_json):
    """
    Archiva las noticias antiguas de noticias/ a noticias_ant/
    y actualiza el JSON de noticias antiguas
    """
    print("\n📦 Archivando noticias antiguas...")
    print("-" * 50)
    
    # Crear carpeta de archivo si no existe
    Path('noticias_ant').mkdir(exist_ok=True)
    
    # Verificar si existe la carpeta de noticias actuales
    if not Path('noticias').exists():
        print("ℹ️  No hay noticias actuales para archivar")
        return
    
    # Cargar historial completo
    archivo_historial = 'historial_completo.json'
    historial = {}
    if Path(archivo_historial).exists():
        try:
            with open(archivo_historial, 'r', encoding='utf-8') as f:
                historial = json.load(f)
        except:
            historial = {}
    
    # Cargar JSON de noticias antiguas si existe
    archivo_json = 'noticias_antiguas.json'
    noticias_antiguas = []
    ids_ya_archivados = set()
    
    if Path(archivo_json).exists():
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                data_antiguas = json.load(f)
                noticias_antiguas = data_antiguas.get('noticias', [])
                # Obtener IDs ya archivados para no duplicar
                ids_ya_archivados = {n['id'] for n in noticias_antiguas if 'id' in n}
            print(f"✅ Cargadas {len(noticias_antiguas)} noticias antiguas existentes")
        except Exception as e:
            print(f"⚠️  Error al cargar {archivo_json}: {e}")
            noticias_antiguas = []
    
    # Obtener lista de archivos HTML en noticias/
    archivos_html = list(Path('noticias').glob('*.html'))
    
    if not archivos_html:
        print("ℹ️  No hay archivos HTML para archivar")
        return
    
    # Recopilar IDs de noticias actuales para no archivarlas
    ids_actuales = set()
    if 'noticia_principal' in noticias_actuales_json:
        ids_actuales.add(noticias_actuales_json['noticia_principal']['id'])
    if 'noticias_secundarias' in noticias_actuales_json:
        for noticia in noticias_actuales_json['noticias_secundarias']:
            ids_actuales.add(noticia['id'])
    if 'noticias_lo_ultimo' in noticias_actuales_json:
        for noticia in noticias_actuales_json['noticias_lo_ultimo']:
            ids_actuales.add(noticia['id'])
    
    # Construir conjunto de nombres ya archivados para evitar
    # re-mover o tocar páginas que ya fueron enviadas a noticias_ant
    nombres_ya_archivados = {p.name for p in Path('noticias_ant').glob('*.html')}

    # Mover archivos HTML antiguos y guardar sus datos
    archivados = 0
    for archivo in archivos_html:
        # Obtener el ID del archivo (nombre sin extensión)
        id_noticia = archivo.stem
        
        # Si este ID NO está en las noticias actuales, archivar
        if id_noticia not in ids_actuales:
            # Si ya existe una versión archivada con el mismo nombre,
            # asumimos que ya fue procesado y se mantiene su redirección.
            if archivo.name in nombres_ya_archivados:
                print(f"ℹ️  {archivo.name} ya está archivado, se mantiene su redirección.")
                continue

            # Buscar datos en el historial
            if id_noticia in historial and id_noticia not in ids_ya_archivados:
                noticia_datos = historial[id_noticia].copy()
                noticia_datos['fecha_archivo'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                noticias_antiguas.append(noticia_datos)
                print(f"📦 Archivado con datos: {archivo.name}")
            else:
                # Si no está en historial, guardar solo info básica
                if id_noticia not in ids_ya_archivados:
                    noticias_antiguas.append({
                        'id': id_noticia,
                        'fecha_archivo': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'nota': 'Archivado sin datos completos del historial'
                    })
                    print(f"📦 Archivado sin datos: {archivo.name}")
                else:
                    print(f"📦 Archivado (ya registrado): {archivo.name}")
            
            # Mover el archivo a noticias_ant
            destino = Path('noticias_ant') / archivo.name
            shutil.move(str(archivo), str(destino))
            archivados += 1

            # Crear una página de redirección en la ruta original
            # para que los enlaces antiguos (noticias/slug.html)
            # sigan funcionando y apunten al archivo en noticias_ant/.
            redireccion_path = Path('noticias') / archivo.name
            try:
                with open(redireccion_path, 'w', encoding='utf-8') as f:
                    f.write(PLANTILLA_REDIRECCION.format(archivo=archivo.name))
                print(f"🔁 Creada página de redirección: {redireccion_path}")
            except Exception as e:
                print(f"⚠️  No se pudo crear la página de redirección para {archivo.name}: {e}")
    
    if archivados > 0:
        print(f"\n✅ {archivados} archivos movidos a noticias_ant/")
        
        # Guardar JSON actualizado
        data_guardar = {
            'ultima_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_noticias': len(noticias_antiguas),
            'noticias': noticias_antiguas,
            'info': 'Este archivo contiene el historial de todas las noticias archivadas'
        }
        
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(data_guardar, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON actualizado: {archivo_json} ({len(noticias_antiguas)} noticias)")
    else:
        print("ℹ️  No hay noticias para archivar (todas son actuales)")


def main():
    """Función principal que genera todas las páginas"""
    print("🚀 Generador de Páginas HTML - RED")
    print("=" * 50)
    
    # Cargar JSON
    try:
        with open('noticias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON cargado correctamente")
    except Exception as e:
        print(f"❌ Error al cargar noticias.json: {e}")
        return
    
    # GUARDAR NOTICIAS ACTUALES EN EL HISTORIAL
    guardar_noticias_en_historial(data)
    
    # ARCHIVAR NOTICIAS ANTIGUAS ANTES DE GENERAR LAS NUEVAS
    archivar_noticias_antiguas(data)
    
    # Crear carpeta noticias si no existe
    Path('noticias').mkdir(exist_ok=True)
    print("\n📝 Preparando generación de noticias nuevas...")
    print("✅ Carpeta 'noticias/' verificada")
    
    config = data['config']
    noticias_generadas = 0
    
    # Recopilar todas las noticias
    todas_noticias = []
    
    # Noticia principal
    if 'noticia_principal' in data:
        todas_noticias.append(data['noticia_principal'])
    
    # Noticias secundarias
    if 'noticias_secundarias' in data:
        todas_noticias.extend(data['noticias_secundarias'])
    
    # Lo último
    if 'noticias_lo_ultimo' in data:
        todas_noticias.extend(data['noticias_lo_ultimo'])
    
    # Generar páginas
    print(f"\n📝 Generando {len(todas_noticias)} páginas...")
    print("-" * 50)
    
    for noticia in todas_noticias:
        try:
            html = generar_pagina_noticia(noticia, config)
            filename = f"noticias/{noticia['id']}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"✅ {filename} - {noticia['titulo'][:50]}...")
            noticias_generadas += 1
            
        except Exception as e:
            print(f"❌ Error al generar {noticia.get('id', 'unknown')}: {e}")
    
    print("-" * 50)
    print(f"\n🎉 ¡Listo! {noticias_generadas} páginas generadas correctamente")
    print(f"📁 Ubicación: ./noticias/")
    print("\n💡 Ahora puedes abrir index.html y hacer clic en las noticias")


if __name__ == "__main__":
    main()

