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
      <!-- Placeholder image - Replace with your own -->
      <img src="https://placehold.co/600x400/EEE/31343C?text=Project+1" alt="Project 1">
    </div>
    <div class="project-content">
      <h3 class="project-title">Bayesian Network Inference Engine</h3>
      <div class="project-description">
        <p>
          A Python library for exact and approximate inference in Bayesian Networks. 
          This project implements variable elimination and belief propagation algorithms, 
          optimized for handling large-scale probabilistic graphical models.
        </p>
        <p>
          It includes visualization tools for network structures and posterior distributions.
        </p>
        <a href="#" class="project-link">View Project &rarr;</a>
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

