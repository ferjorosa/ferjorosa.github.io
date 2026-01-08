---
layout: page
title: Projects
permalink: /projects/
nav: Projects
---

<style>
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
  font-weight: bold;
}
.project-description {
  color: #666;
  line-height: 1.6;
}
.project-link {
  display: inline-block;
  margin-top: 10px;
  font-weight: bold;
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
      <h3 class="project-title">BNE Hemeroteca OCR Dataset (XIX Century)</h3>
      <div class="project-description">
        <p>
          Full text OCR and page images for 19th century Spanish publications from the 
          <a href="https://hemerotecadigital.bne.es/" target="_blank">Biblioteca Nacional de España (BNE) - Hemeroteca Digital</a>. 
          This dataset contains over 40,000 PDF documents, more than 800,000 pages, and over 800 million text tokens.
        </p>
        <p>
          Processed using <a href="https://huggingface.co/allenai/olmOCR-2-7B-1025-FP8" target="_blank">allenai/olmOCR-2-7B-1025-FP8</a>, 
          the dataset covers 20 thematic collections from the 19th century, including literature, science, politics, and culture. 
          It enables OCR benchmarking, text retrieval, RAG systems, and LLM pretraining on historical Spanish text.
        </p>
        <div style="margin-top: 10px;">
          <a href="https://huggingface.co/datasets/ferjorosa/bne-hemeroteca-ocr-xix" target="_blank" title="HuggingFace Dataset" style="margin-right: 15px;">
            <img src="https://huggingface.co/front/assets/huggingface_logo.svg" 
                 alt="HuggingFace" 
                 style="width:24px; height:24px; vertical-align:middle;">
          </a>
          <a href="https://github.com/ferjorosa/bne-hemeroteca-data" target="_blank" title="GitHub">
            <img src="https://cdn.simpleicons.org/github" alt="GitHub" style="width:24px; height:24px;">
          </a>
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

