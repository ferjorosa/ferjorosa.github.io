---
layout: page
title: My Setup
permalink: /my_setup/
nav: My Setup
---

<style>
/* Hide page title for comparison */
.page-content h1:first-of-type:not(.setup-section-title),
.page-header h1,
h1.page-heading {
  display: none;
}
/* Match page title size with blog page */
.page-content h1:not(.setup-section-title),
h1.page-heading {
  font-size: 2rem;
  font-weight: 400;
}
/* Align setup list with blog post list - match home layout spacing */
.page-content {
  margin-top: 0;
  padding-top: 0;
}
.setup-list {
  margin-top: 0;
  padding-top: 0;
}
.setup-section {
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}
.setup-section:last-child {
  border-bottom: none;
}
.setup-section-title {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 400;
  color: #333;
}
.setup-image {
  height: 300px;
  width: auto;
  max-width: 100%;
  display: block;
  margin: 0 auto;
}
.setup-images-container {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  align-items: flex-start;
  margin: 1.5rem 0;
  flex-wrap: wrap;
}
.setup-images-container .setup-image {
  flex: 0 1 auto;
  margin: 0;
}
@media (max-width: 768px) {
  .setup-images-container {
    flex-direction: column;
    align-items: center;
  }
}
.setup-image-caption {
  text-align: center;
  margin-top: 10px;
  font-style: italic;
  color: #666;
}
.setup-specs {
  margin-top: 1rem;
  line-height: 1.8;
}
.setup-specs strong {
  font-weight: 500;
}
.setup-description {
  margin-bottom: 1.5rem;
  line-height: 1.6;
  color: #333;
}
.setup-description a {
  color: #007bff;
  text-decoration: none;
}
.setup-description a:hover {
  text-decoration: underline;
}
</style>

<div class="setup-list">

  <!-- AI Research Setup -->
  <div class="setup-section">
    <h3 class="setup-section-title">AI Research Setup</h3>
    
    <div class="setup-description">
      <p>I bought my PC pre-built from <a href="https://epical-q.com/" target="_blank">Epical-Q</a> and simply added another SSD.</p>
    </div>

    <img src="/assets/my_setup/Epical-Q-ProBex-1.webp" alt="Epical-Q ProBex PC" class="setup-image">

    <div class="setup-image-caption">This bad boy can generate so much heat</div>

    <div class="setup-specs">
      <p><strong>Processing Power:</strong></p>
      <ul>
        <li><strong>CPU</strong>: Intel Core i9 14900KF</li>
        <li><strong>GPU</strong>: NVIDIA RTX 5090 32GB (MSI Ventus)</li>
        <li><strong>Memory</strong>: 2x 32GB DDR5 6000MHz</li>
        <li><strong>Storage</strong>: 2x Samsung 990 EVO Plus 2TB NVMe PCIe 4.0</li>
      </ul>

      <p><strong>System:</strong></p>
      <ul>
        <li><strong>Motherboard</strong>: MSI Z790 GAMING PLUS WIFI D5</li>
        <li><strong>Cooling</strong>: Valkyrie-A 360mm AIO Liquid Cooling</li>
        <li><strong>Power Supply</strong>: ASUS ROG THOR 1200W 80+ Platinum Modular</li>
        <li><strong>Case</strong>: Cougar Duoface PRO RGB Black</li>
      </ul>
    </div>
  </div>

  <!-- 3D Printing Setup -->
  <div class="setup-section">
    <h3 class="setup-section-title">3D Printing Setup</h3>
    
    <div class="setup-description">
      <p>I use a Bambu Lab A1 Mini. It is easy to use with great output quality, though I'd recommend having a separate room since it generates a moderate level of noise. I use a Creality Space Pi for drying filament.</p>
    </div>

    <div class="setup-images-container">
      <img src="/assets/my_setup/bambu-lab-a1-mini.png" alt="Bambu Lab A1 Mini" class="setup-image">
      <img src="/assets/my_setup/crealty_space_pi.webp" alt="Creality Space Pi Filament Dryer" class="setup-image">
    </div>

    <div class="setup-image-caption">Little noise machine and its drying companion</div>
  </div>

</div>

