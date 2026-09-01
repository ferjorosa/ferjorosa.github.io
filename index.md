---
layout: page
title: Fernando Rodriguez
# permalink: /about/  <-- Removed permalink so it defaults to index (/)
# nav: About <-- Removed nav since this is home, but user wants "Projects, Blog, Blog Archive" in menu.
---

<style>
  .post-header {
    display: none;
  }
  .profile-header {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
  }
  .profile-pic-container {
    flex-shrink: 0;
    margin-right: 1.5rem;
  }
  .profile-pic {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
  }
  .profile-desc {
    display: flex;
    flex-direction: column;
  }
  .profile-desc h1 {
    font-size: 2rem;
    margin: 0;
    border-bottom: none;
    padding-bottom: 0;
  }
  .profile-desc h2 {
    font-size: 1.2rem;
    font-weight: normal;
    margin: 0.5rem 0 1rem 0;
    color: #555;
  }
  .social-icons a {
    margin-right: 10px;
  }
  .social-icons img {
    width: 24px;
    height: 24px;
  }
  .project-item {
    display: flex;
    margin-top: 1rem;
    align-items: flex-start;
    padding-top: 1rem;
    border-top: 1px solid #eee;
  }
  .project-image {
    flex: 0 0 120px;
    margin-right: 25px;
  }
  .project-image img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
  .project-content {
    flex: 1;
  }
  .project-title {
    margin-top: 0;
    margin-bottom: 0.4rem;
    font-size: 1.2rem;
    font-weight: 500;
  }
  .project-description {
    color: #666;
    line-height: 1.5;
    font-size: 0.95rem;
  }
  @media (max-width: 768px) {
    .project-item {
      flex-direction: column;
    }
    .project-image {
      margin-right: 0;
      margin-bottom: 15px;
      flex: 0 0 auto;
      width: 120px;
    }
  }
</style>

<div class="profile-header">
  <div class="profile-pic-container">
    <img src="/assets/about/profile_400.jpg" alt="Profile photo" class="profile-pic">
  </div>
  <div class="profile-desc">
    <h1>Fernando Rodriguez Sanchez</h1>
    <h2><i>Building cool things and writing about them</i></h2>
    <div class="social-icons">
        <a href="https://scholar.google.es/citations?hl=es&user=iYjOAYQAAAAJ" title="Google Scholar" target="_blank" style="margin-right: 10px;">
        <svg role="img" viewBox="0 0 24 24" style="width:24px;vertical-align:middle; fill: #4285F4;" 
                xmlns="http://www.w3.org/2000/svg">
            <title>Google Scholar</title>
            <path d="M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/>
        </svg>
        </a>
        <a href="https://github.com/ferjorosa" title="GitHub" target="_blank" style="margin-right: 10px;">
        <svg role="img" viewBox="0 0 24 24" style="width:24px;vertical-align:middle; fill: #181717;"
                xmlns="http://www.w3.org/2000/svg">
            <title>GitHub</title>
            <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
        </svg>
        </a>
        <a href="https://huggingface.co/ferjorosa" title="HuggingFace">
        <img src="https://huggingface.co/front/assets/huggingface_logo.svg" 
        alt="HuggingFace" 
        style="width:24px; height:24px; vertical-align:middle;">
        </a>
        <!-- <a href="https://twitter.com/ferjorosa" title="Twitter"><img src="https://cdn.simpleicons.org/x" alt="X"></a> -->
        <a href="https://twitter.com/ferjorosa" target="_blank" style="margin-right: 10px;">
        <svg role="img" viewBox="0 0 24 24" style="width:24px;vertical-align:middle; fill: #1DA1F2;" 
                xmlns="http://www.w3.org/2000/svg">
            <title>Twitter</title>
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
        </svg>
        </a>
        <a href="https://www.linkedin.com/in/ferjorosa/" title="LinkedIn" target="_blank" style="margin-right: 10px;">
        <svg role="img" viewBox="0 0 24 24" style="width:24px;vertical-align:middle; fill: #0077B5;" 
                xmlns="http://www.w3.org/2000/svg">
            <title>LinkedIn</title>
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
        </a>
    </div>
  </div>
</div>

I work as a Senior AI Engineer at <a href="https://www.medvelle.com/">Medvelle</a>, where I focus on Software Engineering and Agentic Reasoning. Before joining Medvelle, I worked as a Lead AI Engineer at Aily Labs and Senior Research Scientist at Nielsen IQ.

I hold a PhD in Artificial Intelligence from the Polytechnic University of Madrid, where I worked on learning Bayesian networks with latent variables for clustering and density estimation. My advisors were [Pedro Larrañaga](https://dia.fi.upm.es/personaldia/pedro-larranaga/) and [Concha Bielza](https://muia.dia.fi.upm.es/es/personal/bielza-lozoya-concepcion/).

In my spare time, I run [Cynosural AI](https://cynosural.org/), an AI research initiative from Spain. We are currently collaborating with the Spanish Ministry of Culture to make historical archives more accessible. I also write about AI on my [blog](https://ferjorosa.github.io/blog/) and enjoy 3D printing and painting <a href="https://x.com/ferjorosa/status/1936136612317938016">Warhammer miniatures</a>.

<!-- <div style="text-align: center; margin-top: 1.5rem;">
  <a href="https://cynosural.org/" target="_blank">
    <img src="/assets/cynosural/cynosural_logo_v4.png" alt="Cynosural AI" style="width: 120px; height: auto; opacity: 0.9; transition: opacity 0.2s;">
  </a>
<br>
  Cynosural AI
</div> -->