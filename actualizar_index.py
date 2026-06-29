#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualizador automático del index.html
Lee noticias.json y genera el index.html con todas las noticias
Autor: Trickzz.sh
"""

import json
from datetime import datetime
from pathlib import Path


# Plantilla HTML del index.html
PLANTILLA_INDEX = """<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="version" content="2.0-IA-NOTICIAS">
    <link rel="icon" type="image/png" href="IMG/footer.png">
    <title>RED - Tu fuente confiable de información</title>
    <!-- Importamos fuentes elegantes de Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Roboto:wght@300;400;500;700&display=swap"
        rel="stylesheet">

    <style>
        /* VARIABLES Y CONFIGURACIÓN BASE */
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
            cursor: pointer;
        }}

        a:hover {{
            color: var(--brand-rojo);
        }}

        /* LAYOUT GENERAL */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* HEADER */
        .header-main {{
            padding: 25px 0;
            text-align: center;
            cursor: pointer;
            position: relative;
            /* Para volver al home */
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



        /* GRID PRINCIPAL DE NOTICIAS (HOME) */
        .news-grid {{
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 40px;
            margin-top: 30px;
            margin-bottom: 50px;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
        }}

        /* ESTILOS DE ARTÍCULOS (PREVIEW) */
        .article {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            position: relative;
        }}

        .article::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(to right, var(--brand-rojo) 0%, var(--brand-rojo-oscuro) 50%, var(--brand-gris) 100%);
        }}

        .article:last-child::after {{
            display: none;
        }}

        .article-kicker {{
            background: linear-gradient(to right, var(--brand-rojo) 0%, var(--brand-rojo) 25%, var(--brand-rojo-oscuro) 50%, var(--brand-rojo-oscuro) 75%, var(--brand-rojo-oscuro) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: block;
        }}

        .article-title {{
            font-family: var(--sans-font);
            font-weight: 700;
            line-height: 1.1;
            color: var(--brand-dark);
            margin-top: 30px; margin-bottom: 50px;
        }}

        .article-title:hover {{
            color: var(--brand-rojo);
            cursor: pointer;
        }}

        .article-summary {{
            font-size: 15px;
            color: #555;
            margin-bottom: 15px;
        }}

        .article-author {{
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
        }}

        .article-author strong {{
            color: var(--brand-dark);
        }}

        .article-img {{
            width: 100%;
            height: auto;
            display: block;
            margin-bottom: 15px;
            filter: brightness(0.95);
            transition: filter 0.3s;
            cursor: pointer;
        }}

        .article-img:hover {{
            filter: brightness(1);
        }}

        .hero-article .article-title {{
            font-size: 42px;
        }}

        .hero-article .article-summary {{
            font-size: 18px;
            line-height: 1.6;
        }}

        .list-article .article-title {{
            font-size: 20px;
        }}

        .list-article .article-img {{
            aspect-ratio: 16/9;
            object-fit: contain;
        }}

        /* SIDEBAR Y ANUNCIO */
        .sidebar-title {{
            font-size: 14px;
            font-weight: 900;
            text-transform: uppercase;
            border-bottom: 2px solid var(--brand-dark);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}


        .opinion-item {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px dotted #ccc;
            padding-bottom: 15px;
        }}

        .opinion-img {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin-right: 15px;
            object-fit: contain;
        }}

        .opinion-content h4 {{
            font-family: var(--sans-font);
            font-size: 16px;
            margin-bottom: 4px;
        }}

        .opinion-author {{
            font-size: 11px;
            text-transform: uppercase;
            background: linear-gradient(to right, var(--brand-rojo) 0%, var(--brand-rojo-oscuro) 50%, var(--brand-rojo-oscuro) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: bold;
            display: inline-block;
        }}

        /* NEWSLETTER CTA + MODAL */
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
            .news-grid {{
                grid-template-columns: 1fr;
            }}

            .sidebar-col {{
                display: none;
            }}

            /* Simplificado para tablet */
        }}

        @media (max-width: 768px) {{
            .sidebar-col {{
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

            /* Sidebar vuelve abajo en móvil */
        }}
    </style>
</head>

<body>

    <!-- HEADER LOGO -->
    <header class="header-main">
        <div class="container">
            <a href="index.html" class="logo-container">
                <img src="IMG/footer.png" alt="RED" class="logo-img">
            </a>
            <div class="collaboration-line">
                En colaboración con <strong>Diario El Mundo</strong>
            </div>
            <div class="date-line">
                {fecha_actualizacion}
            </div>
        </div>
    </header>


    <!-- CONTENIDO PRINCIPAL -->
    <main class="container">

        <!-- ======================= NUEVAS NOTICIAS DE IA ======================= -->
        <div id="home-view">
            <div class="news-grid">

                <!-- COLUMNA 1: PRINCIPAL -->
                <section class="main-col">
{noticia_principal}

{noticias_secundarias_main}
                </section>

                <!-- COLUMNA 2: SECUNDARIAS -->
                <section class="center-col">
                    <div class="sidebar-title">Más Noticias de RED</div>

{noticias_secundarias_center}

{noticias_lo_ultimo}
                </section>

            </div>
        </div>

    </main>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-left">
                    <div class="footer-logo">
                        <img src="IMG/footer.png" alt="RED" class="logo-img-footer">
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

</html>"""


def generar_articulo_principal(noticia):
    """Genera el HTML para la noticia principal"""
    return f"""                    <article class="article hero-article">
                        <span class="article-kicker">{noticia.get('categoria', 'Actualidad')}</span>
                        <a href="noticias/{noticia['id']}.html">
                            <img src="{noticia['imagen']}"
                                alt="{noticia['titulo']}" class="article-img">
                        </a>
                        <h1 class="article-title"><a href="noticias/{noticia['id']}.html">{noticia['titulo']}</a></h1>
                        <p class="article-summary">
                            {noticia['resumen']}
                        </p>
                        <div class="article-author">
                            Por <strong>Redacción RED</strong> | San Salvador
                        </div>
                    </article>"""


def generar_articulo_secundario_main(noticia):
    """Genera el HTML para una noticia secundaria en la columna principal"""
    return f"""                    <article class="article" style="margin-top: 30px;">
                        <a href="noticias/{noticia['id']}.html">
                            <img src="{noticia['imagen']}" alt="{noticia['titulo']}"
                                class="article-img">
                        </a>
                        <span class="article-kicker">{noticia.get('categoria', 'Actualidad')}</span>
                        <h2 class="article-title" style="font-size: 28px;"><a
                                href="noticias/{noticia['id']}.html">{noticia['titulo']}</a></h2>
                        <p class="article-summary" style="font-size: 16px;">
                            {noticia['resumen']}
                        </p>
                        <div class="article-author">
                            Por <strong>Redacción RED</strong> | San Salvador
                        </div>
                    </article>"""


def generar_articulo_lista(noticia):
    """Genera el HTML para una noticia en lista (columna central)"""
    return f"""                    <article class="article list-article">
                        <a href="noticias/{noticia['id']}.html">
                            <img src="{noticia['imagen']}"
                                alt="{noticia['titulo']}" class="article-img">
                        </a>
                        <span class="article-kicker">{noticia.get('categoria', 'Actualidad')}</span>
                        <h3 class="article-title"><a href="noticias/{noticia['id']}.html">{noticia['titulo']}</a></h3>
                        <p class="article-summary" style="font-size: 14px; margin-top: 8px;">
                            {noticia['resumen']}
                        </p>
                    </article>"""


def main():
    """Función principal que actualiza el index.html"""
    print("🔄 Actualizador de Index.html - RED NOTICIAS")
    print("=" * 50)
    
    # Cargar JSON de noticias
    try:
        with open('noticias.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON de noticias cargado correctamente")
    except Exception as e:
        print(f"❌ Error al cargar noticias.json: {e}")
        return
    
    config = data.get('config', {})
    
    # Preparar variables de la plantilla
    edicion = config.get('edicion', 'Edición El Salvador')
    fecha_actualizacion = config.get('fecha_actualizacion', datetime.now().strftime('%A, %d de %B de %Y'))
    
    # Extraer fecha corta para el sidebar
    try:
        # Intentar extraer una fecha corta del formato
        fecha_corta = datetime.now().strftime('%d/%m/%Y')
    except:
        fecha_corta = '17/12/2025'
    
    # Generar HTML de las noticias
    noticia_principal_html = ""
    noticias_secundarias_main_html = ""
    noticias_secundarias_center_html = ""
    noticias_lo_ultimo_html = ""
    
    total_noticias = 0
    
    # Noticia principal
    if 'noticia_principal' in data:
        noticia_principal_html = generar_articulo_principal(data['noticia_principal'])
        total_noticias += 1
        print("✅ Noticia principal procesada")
    
    # Noticias secundarias (repartidas entre main y center)
    if 'noticias_secundarias' in data:
        secundarias = data['noticias_secundarias']
        # Primera noticia secundaria va a main-col
        if len(secundarias) > 0:
            noticias_secundarias_main_html = generar_articulo_secundario_main(secundarias[0])
            total_noticias += 1
        
        # El resto van a center-col
        for noticia in secundarias[1:]:
            noticias_secundarias_center_html += generar_articulo_lista(noticia) + "\n"
            total_noticias += 1
        
        print(f"✅ {len(secundarias)} noticias secundarias procesadas")
    
    # Noticias de "lo último"
    if 'noticias_lo_ultimo' in data:
        for noticia in data['noticias_lo_ultimo']:
            noticias_lo_ultimo_html += generar_articulo_lista(noticia) + "\n"
            total_noticias += 1
        print(f"✅ {len(data['noticias_lo_ultimo'])} noticias de 'Lo último' procesadas")
    
    # Generar HTML completo
    html_final = PLANTILLA_INDEX.format(
        edicion=edicion,
        fecha_actualizacion=fecha_actualizacion,
        noticia_principal=noticia_principal_html,
        noticias_secundarias_main=noticias_secundarias_main_html,
        noticias_secundarias_center=noticias_secundarias_center_html,
        noticias_lo_ultimo=noticias_lo_ultimo_html,
        total_noticias=total_noticias,
        fecha_corta=fecha_corta
    )
    
    # Guardar index.html
    try:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_final)
        print("\n✅ index.html actualizado correctamente")
        print(f"📊 Total de noticias: {total_noticias}")
        print("💡 El archivo está listo para ser usado")
    except Exception as e:
        print(f"❌ Error al guardar index.html: {e}")


if __name__ == "__main__":
    main()

