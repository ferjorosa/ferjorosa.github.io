---
layout: page
title: Projects
permalink: /projects/
nav: Projects
---

<style>
/* Hide page title for comparison */
.page-content h1:first-of-type:not(.project-title),
.page-header h1,
h1.page-heading {
  display: none;
}
/* Match page title size with blog page */
.page-content h1:not(.project-title),
h1.page-heading {
  font-size: 2rem;
  font-weight: 400;
}
/* Align project list with blog post list - match home layout spacing */
.page-content {
  margin-top: 0;
  padding-top: 0;
}
.project-list {
  margin-top: 0;
  padding-top: 0;
}
.project-item:first-child {
  margin-top: 0;
  padding-top: 0;
}
.project-item {
  display: flex;
  margin-bottom: 3rem;
  align-items: flex-start;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}
.project-item:last-child {
  border-bottom: none;
}
.project-image {
  flex: 0 0 250px;
  margin-right: 30px;
}
.project-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  object-fit: cover;
}
.project-content {
  flex: 1;
}
.project-title {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
  font-weight: 400;
}
.project-description {
  color: #666;
  line-height: 1.6;
}
.project-link {
  display: inline-block;
  margin-top: 10px;
  font-weight: 400;
  color: #007bff; /* Example blue, matches typical links */
  text-decoration: none;
}
.project-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .project-item {
    flex-direction: column;
  }
  .project-image {
    margin-right: 0;
    margin-bottom: 20px;
    flex: 0 0 auto;
    width: 100%;
    max-width: 400px; /* Limit width on mobile */
  }
}
</style>

<div class="project-list">

  <!-- Project 1 -->
  <div class="project-item">
    <div class="project-image">
      <img src="/assets/projects/bne_hemeroteca/BNE_logo.png" alt="BNE Hemeroteca OCR">
    </div>
    <div class="project-content">
      <h3 class="project-title">19th-Century Spanish OCR Dataset</h3>
      <div class="project-description">
        <p>
          A dataset of over 40,000 PDF documents comprising more than 800,000 pages and over 800 million text tokens, drawn from 19th-century Spanish publications in the 
          <a href="https://hemerotecadigital.bne.es/" target="_blank">Biblioteca Nacional de España (BNE) – Hemeroteca Digital</a>. 
        </p>
        <div style="margin-top: 15px;">
          <div style="margin-bottom: 8px; display: flex; gap: 20px; flex-wrap: wrap;">
            <!-- <a href="#" class="project-link">Blog post</a> -->
            <a href="https://huggingface.co/datasets/ferjorosa/bne-hemeroteca-ocr-xix" target="_blank" class="project-link" style="display: inline-flex; align-items: center; gap: 8px;">
              <img src="https://huggingface.co/front/assets/huggingface_logo.svg" 
                   alt="HuggingFace" 
                   style="width:20px; height:20px;">
              Dataset
            </a>
            <a href="https://github.com/ferjorosa/bne-hemeroteca-data" target="_blank" class="project-link" style="display: inline-flex; align-items: center; gap: 8px;">
              <img src="https://cdn.simpleicons.org/github" alt="GitHub" style="width:20px; height:20px;">
              Code
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Project 2 
  <div class="project-item">
    <div class="project-image">
      <img src="https://placehold.co/600x400/EEE/31343C?text=Project+2" alt="Project 2">
    </div>
    <div class="project-content">
      <h3 class="project-title">LLM Reasoning Assistant</h3>
      <div class="project-description">
        <p>
          An experimental interface exploring how Large Language Models can perform multi-step reasoning.
          The system prompts models to break down complex problems into smaller, manageable steps
          and verifies consistency across reasoning chains.
        </p>
        <a href="#" class="project-link">View Project &rarr;</a>
      </div>
    </div>
  </div>
  -->

  <!-- Project 3 
  <div class="project-item">
    <div class="project-image">
      <img src="https://placehold.co/600x400/EEE/31343C?text=Project+3" alt="Project 3">
    </div>
    <div class="project-content">
      <h3 class="project-title">Miniature Painting Tracker</h3>
      <div class="project-description">
        <p>
          A web application to track progress on miniature painting projects. 
          Features include color recipe management, time tracking, and a gallery for completed models.
          Built with React and Firebase.
        </p>
        <a href="#" class="project-link">View Project &rarr;</a>
      </div>
    </div>
  </div>
  -->

</div>

