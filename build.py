#!/usr/bin/env python3
"""
Sifat Notes — static site builder.
Stitches partials/header.html (+ a track-specific sidebar-{ml,dl,nlp}.html for
course pages, footer.html for the home page only) and per-page content
fragments from content/ into final pages using page_template.html /
home_template.html. Course pages are written into ml/, dl/, nlp/ subfolders
by topic/track; the home page stays at the project root.
Run: python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
PARTIALS = ROOT / "partials"
CONTENT = ROOT / "content"

PAGE_TEMPLATE = (ROOT / "page_template.html").read_text()
HOME_TEMPLATE = (ROOT / "home_template.html").read_text()

HEADER = (PARTIALS / "header.html").read_text()
SIDEBAR_ML = (PARTIALS / "sidebar-ml.html").read_text()
SIDEBAR_DL = (PARTIALS / "sidebar-dl.html").read_text()
SIDEBAR_NLP = (PARTIALS / "sidebar-nlp.html").read_text()
FOOTER = (PARTIALS / "footer.html").read_text()

SIGMOID_JS = """<script>
  let sigmoidChart;
  function sigmoidData(k){
    const pts = [];
    for(let x=-6; x<=6; x+=0.25){ pts.push({x:x, y:1/(1+Math.exp(-k*x))}); }
    return pts;
  }
  function initSigmoidChart(){
    const ctx = document.getElementById('sigmoidChart');
    if(!ctx) return;
    const styles = getComputedStyle(document.documentElement);
    sigmoidChart = new Chart(ctx, {
      type: 'line',
      data: { datasets: [{
        label: 'sigma(x) = 1 / (1 + e^-kx)',
        data: sigmoidData(1),
        borderColor: styles.getPropertyValue('--primary').trim(),
        backgroundColor: 'transparent', borderWidth: 2.5, pointRadius: 0, tension: 0.1
      }]},
      options: {
        responsive: true, animation: { duration: 200 },
        scales: {
          x: { type: 'linear', title:{display:true,text:'x'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} },
          y: { min:0, max:1, title:{display:true,text:'sigma(x)'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} }
        },
        plugins: { legend: { display:false } }
      }
    });
  }
  function updateSigmoid(){
    const k = parseFloat(document.getElementById('kSlider').value);
    document.getElementById('kVal').textContent = k.toFixed(1);
    sigmoidChart.data.datasets[0].data = sigmoidData(k);
    sigmoidChart.update();
  }
  window.addEventListener('DOMContentLoaded', initSigmoidChart);
</script>"""

GB_RESIDUAL_JS = """<script>
  let gbResidualChart;
  function gbResidualData(lr){
    const pts = [];
    const r0 = 16.25;
    for(let t=0; t<=30; t++){ pts.push({x:t, y: r0 * Math.pow(1-lr, t)}); }
    return pts;
  }
  function initGBResidualChart(){
    const ctx = document.getElementById('gbResidualChart');
    if(!ctx) return;
    const styles = getComputedStyle(document.documentElement);
    gbResidualChart = new Chart(ctx, {
      type: 'line',
      data: { datasets: [{
        label: 'Remaining residual (illustrative)',
        data: gbResidualData(0.1),
        borderColor: styles.getPropertyValue('--primary').trim(),
        backgroundColor: 'transparent', borderWidth: 2.5, pointRadius: 0, tension: 0.1
      }]},
      options: {
        responsive: true, animation: { duration: 200 },
        scales: {
          x: { type: 'linear', title:{display:true,text:'Boosting round'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} },
          y: { min:0, max:17, title:{display:true,text:'Residual magnitude'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} }
        },
        plugins: { legend: { display:false } }
      }
    });
  }
  function updateGBResidual(){
    const lr = parseFloat(document.getElementById('gbLrSlider').value);
    document.getElementById('gbLrVal').textContent = lr.toFixed(2);
    gbResidualChart.data.datasets[0].data = gbResidualData(lr);
    gbResidualChart.update();
  }
  window.addEventListener('DOMContentLoaded', initGBResidualChart);
</script>"""

KMEANS_JS = """<script>
  let kmeansChart;
  function initKmeansChart(){
    const ctx = document.getElementById('kmeansChart');
    if(!ctx) return;
    const styles = getComputedStyle(document.documentElement);
    const clusterColors = [
      styles.getPropertyValue('--primary').trim(),
      styles.getPropertyValue('--secondary').trim(),
      styles.getPropertyValue('--tertiary').trim()
    ];
    const clusters = [
      { points: [[2,3],[2.5,3.5],[1.8,2.6],[3,3.2],[2.2,4],[1.5,3],[2.8,2.8],[2,2.2]], centroid: [2.2,3.0] },
      { points: [[8,8],[8.5,7.5],[9,8.2],[7.8,8.6],[8.3,9],[9.2,7.8],[7.5,7.9],[8.8,8.5]], centroid: [8.4,8.2] },
      { points: [[2,9],[2.6,8.6],[1.8,9.4],[3,9.2],[1.5,8.8],[2.3,9.7],[3.2,8.7]], centroid: [2.3,9.1] }
    ];
    const datasets = [];
    clusters.forEach((c, i) => {
      datasets.push({
        label: 'Cluster ' + (i+1),
        data: c.points.map(p => ({x:p[0], y:p[1]})),
        backgroundColor: clusterColors[i],
        borderColor: clusterColors[i],
        pointRadius: 5,
        pointHoverRadius: 7,
        showLine: false
      });
      datasets.push({
        label: 'Centroid ' + (i+1),
        data: [{x:c.centroid[0], y:c.centroid[1]}],
        backgroundColor: clusterColors[i],
        borderColor: styles.getPropertyValue('--on-background').trim(),
        borderWidth: 2,
        pointStyle: 'star',
        pointRadius: 12,
        pointHoverRadius: 14,
        showLine: false
      });
    });
    kmeansChart = new Chart(ctx, {
      type: 'scatter',
      data: { datasets },
      options: {
        responsive: true, animation: { duration: 300 },
        scales: {
          x: { title:{display:true,text:'Feature 1'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} },
          y: { title:{display:true,text:'Feature 2'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} }
        },
        plugins: {
          legend: {
            display: true,
            labels: {
              color: styles.getPropertyValue('--on-surface').trim(),
              boxWidth: 10,
              font: { size: 10 },
              filter: (item) => item.text.startsWith('Cluster')
            }
          }
        }
      }
    });
  }
  window.addEventListener('DOMContentLoaded', initKmeansChart);
</script>"""

# page_id -> (title, crumbs_html, extra_js)
COURSE_PAGES = {
    "section-01": (
        "1. Introduction to ML",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a>'
        '<span class="mx-2">/</span>'
        '<a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a>'
        '<span class="mx-2">/</span>'
        '<span class="text-[var(--on-background)]">1. Introduction to ML</span>',
        "",
    ),
    "section-02": (
        "2. Learning Styles",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">2. Learning Styles</span>',
        "",
    ),
    "section-03": (
        "3. ML Landscape",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">3. ML Landscape</span>',
        "",
    ),
    "section-04": (
        "4. Tensors & Setup",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">4. Tensors & Setup</span>',
        "",
    ),
    "section-05": (
        "5. Data Gathering",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">5. Data Gathering</span>',
        "",
    ),
    "section-06": (
        "6. Exploratory Data Analysis",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">6. Exploratory Data Analysis</span>',
        "",
    ),
    "section-07": (
        "7. Feature Engineering",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">7. Feature Engineering</span>',
        "",
    ),
    "section-08": (
        "8. Feature Scaling",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">8. Feature Scaling</span>',
        "",
    ),
    "section-09": (
        "9. Encoding Categorical Vars",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">9. Encoding Categorical Vars</span>',
        "",
    ),
    "section-10": (
        "10. Column Transformer & Pipelines",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">10. Column Transformer & Pipelines</span>',
        "",
    ),
    "section-11": (
        "11. Power Transformer",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">11. Power Transformer</span>',
        "",
    ),
    "section-12": (
        "12. Binning & Binarization",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">12. Binning & Binarization</span>',
        "",
    ),
    "section-13": (
        "13. Mixed / Date-Time Data",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">13. Mixed / Date-Time Data</span>',
        "",
    ),
    "section-14": (
        "14. Missing Values",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">14. Missing Values</span>',
        "",
    ),
    "section-15": (
        "15. Outliers",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">15. Outliers</span>',
        "",
    ),
    "section-16": (
        "16. Feature Construction",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">16. Feature Construction</span>',
        "",
    ),
    "section-17": (
        "17. Curse of Dimensionality",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">17. Curse of Dimensionality</span>',
        "",
    ),
    "section-18": (
        "18. PCA",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">18. PCA</span>',
        "",
    ),
    "section-19": (
        "19. Linear Regression",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">19. Linear Regression</span>',
        """<script>
  let gdChart;
  function gdQuadratic(x){ return (x-3)*(x-3); }
  function gdCurveData(){
    const pts = [];
    for(let x=-2; x<=8; x+=0.1){ pts.push({x:x, y:gdQuadratic(x)}); }
    return pts;
  }
  function gdStepData(lr){
    let x = -1.5;
    const pts = [{x:x, y:gdQuadratic(x)}];
    for(let i=0; i<25; i++){
      const grad = 2*(x-3);
      x = x - lr*grad;
      if(!isFinite(x) || Math.abs(x) > 50) break;
      pts.push({x:x, y:gdQuadratic(x)});
    }
    return pts;
  }
  function initGDChart(){
    const ctx = document.getElementById('gdChart');
    if(!ctx) return;
    const styles = getComputedStyle(document.documentElement);
    gdChart = new Chart(ctx, {
      type: 'line',
      data: { datasets: [
        {
          label: 'Loss curve  J(x) = (x - 3)^2',
          data: gdCurveData(),
          borderColor: styles.getPropertyValue('--outline').trim(),
          backgroundColor: 'transparent', borderWidth: 2, pointRadius: 0, tension: 0.25, order: 2
        },
        {
          label: 'Gradient descent steps',
          data: gdStepData(0.1),
          borderColor: styles.getPropertyValue('--primary').trim(),
          backgroundColor: styles.getPropertyValue('--primary').trim(),
          borderWidth: 2, pointRadius: 4, pointHoverRadius: 6, tension: 0, order: 1
        }
      ]},
      options: {
        responsive: true, animation: { duration: 250 },
        scales: {
          x: { type: 'linear', min:-2, max:8, title:{display:true,text:'x'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} },
          y: { min:0, max:30, title:{display:true,text:'J(x)'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} }
        },
        plugins: { legend: { display:true, labels:{ color: styles.getPropertyValue('--on-surface').trim() } } }
      }
    });
  }
  function updateGD(){
    const lr = parseFloat(document.getElementById('lrSlider').value);
    document.getElementById('lrVal').textContent = lr.toFixed(2);
    const steps = gdStepData(lr);
    gdChart.data.datasets[1].data = steps;
    gdChart.update();
    const stepsEl = document.getElementById('gdStepsCount');
    if(stepsEl) stepsEl.textContent = (steps.length - 1);
  }
  window.addEventListener('DOMContentLoaded', initGDChart);
</script>""",
    ),
    "section-20": (
        "20. Polynomial Regression",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">20. Polynomial Regression</span>',
        "",
    ),
    "section-21": (
        "21. Bias-Variance Tradeoff",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">21. Bias-Variance Tradeoff</span>',
        """<script>
  let biasVarianceChart;
  function bvData(complexity){
    const bias = [], variance = [], total = [];
    for(let c=1; c<=10; c++){
      const b = Math.pow(10 - c, 2) * 0.9 + 2;
      const v = Math.pow(c, 2) * 0.9 + 2;
      bias.push({x:c, y:b});
      variance.push({x:c, y:v});
      total.push({x:c, y:b+v});
    }
    return {bias, variance, total};
  }
  function initBiasVarianceChart(){
    const ctx = document.getElementById('biasVarianceChart');
    if(!ctx) return;
    const styles = getComputedStyle(document.documentElement);
    const d = bvData();
    biasVarianceChart = new Chart(ctx, {
      type: 'line',
      data: { datasets: [
        { label: 'Bias²', data: d.bias, borderColor: styles.getPropertyValue('--secondary').trim(), backgroundColor:'transparent', borderWidth:2, pointRadius:0, tension:0.3 },
        { label: 'Variance', data: d.variance, borderColor: styles.getPropertyValue('--tertiary').trim(), backgroundColor:'transparent', borderWidth:2, pointRadius:0, tension:0.3 },
        { label: 'Total error', data: d.total, borderColor: styles.getPropertyValue('--primary').trim(), backgroundColor:'transparent', borderWidth:3, pointRadius:0, tension:0.3 },
        { label: 'Current complexity', data: [], borderColor: styles.getPropertyValue('--error').trim(), backgroundColor: styles.getPropertyValue('--error').trim(), showLine:false, pointRadius:6, pointHoverRadius:7 }
      ]},
      options: {
        responsive: true, animation: { duration: 200 },
        scales: {
          x: { type:'linear', min:1, max:10, title:{display:true,text:'Model complexity'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} },
          y: { title:{display:true,text:'Error'}, grid:{color: styles.getPropertyValue('--outline-variant').trim()} }
        },
        plugins: { legend: { display:true, labels:{ color: styles.getPropertyValue('--on-surface').trim(), boxWidth:12, font:{size:10} } } }
      }
    });
    updateBiasVariance();
  }
  function updateBiasVariance(){
    if(!biasVarianceChart) return;
    const c = parseInt(document.getElementById('complexitySlider').value, 10);
    document.getElementById('complexityVal').textContent = c;
    const b = Math.pow(10 - c, 2) * 0.9 + 2;
    const v = Math.pow(c, 2) * 0.9 + 2;
    biasVarianceChart.data.datasets[3].data = [{x:c, y:b+v}];
    biasVarianceChart.update();
  }
  window.addEventListener('DOMContentLoaded', initBiasVarianceChart);
</script>""",
    ),
    "section-22": (
        "22. Regularization: Ridge, Lasso & Elastic Net",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">22. Regularization</span>',
        "",
    ),
    "section-23": (
        "23. Logistic Regression",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">23. Logistic Regression</span>',
        SIGMOID_JS,
    ),
    "section-24": (
        "24. Classification Metrics",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">24. Classification Metrics</span>',
        "",
    ),
    "section-25": (
        "25. Logistic Regression — Advanced",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">25. Logistic Regression — Advanced</span>',
        "",
    ),
    "section-26": (
        "26. Naive Bayes Classifier",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">26. Naive Bayes Classifier</span>',
        "",
    ),
    "section-27": (
        "27. K-Nearest Neighbors (KNN)",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">27. K-Nearest Neighbors (KNN)</span>',
        "",
    ),
    "section-28": (
        "28. Support Vector Machines (SVM)",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">28. Support Vector Machines (SVM)</span>',
        "",
    ),
    "section-29": (
        "29. Decision Trees",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">29. Decision Trees</span>',
        "",
    ),
    "section-30": (
        "30. Ensemble Learning: Voting",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">30. Ensemble Learning: Voting</span>',
        "",
    ),
    "section-31": (
        "31. Bagging",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">31. Bagging</span>',
        "",
    ),
    "section-32": (
        "32. Random Forest",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">32. Random Forest</span>',
        "",
    ),
    "section-33": (
        "33. AdaBoost",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">33. AdaBoost</span>',
        "",
    ),
    "section-34": (
        "34. Bagging vs Boosting",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">34. Bagging vs Boosting</span>',
        "",
    ),
    "section-35": (
        "35. Gradient Boosting",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">35. Gradient Boosting</span>',
        GB_RESIDUAL_JS,
    ),
    "section-36": (
        "36. XGBoost",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">36. XGBoost</span>',
        "",
    ),
    "section-37": (
        "37. Stacking & Blending",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">37. Stacking & Blending</span>',
        "",
    ),
    "section-38": (
        "38. Clustering: K-Means, Hierarchical & DBSCAN",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">38. Clustering</span>',
        KMEANS_JS,
    ),
    "section-39": (
        "39. Handling Imbalanced Data",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">39. Handling Imbalanced Data</span>',
        "",
    ),
    "section-40": (
        "40. Hyperparameter Tuning with Optuna",
        '<a href="../index.html" class="hover:text-[var(--primary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--primary)]">ML Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">40. Hyperparameter Tuning</span>',
        "",
    ),
}

# page_id prefix -> output subfolder, keeping the site organized by topic/track
TRACK_DIRS = {"section": "ml", "dl": "dl", "nlp": "nlp"}

def build_course_page(page_id, title, crumbs, extra_js, sidebar):
    content = (CONTENT / f"{page_id}.html").read_text()
    html = (PAGE_TEMPLATE
        .replace("{{TITLE}}", title)
        .replace("{{HEADER}}", HEADER)
        .replace("{{SIDEBAR}}", sidebar)
        .replace("{{CRUMBS}}", crumbs)
        .replace("{{CONTENT}}", content)
        .replace("{{EXTRA_JS}}", extra_js)
        .replace("{{ROOT}}", "../")
    )
    track_dir = TRACK_DIRS[page_id.split("-")[0]]
    out_dir = ROOT / track_dir
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{page_id}.html").write_text(html)
    print(f"built {track_dir}/{page_id}.html")

def build_home_page():
    html = (HOME_TEMPLATE
        .replace("{{HEADER}}", HEADER)
        .replace("{{FOOTER}}", FOOTER)
        .replace("{{ROOT}}", "")
    )
    (ROOT / "index.html").write_text(html)
    print("built index.html")

# page_id -> (title, crumbs_html, extra_js) — Deep Learning track
DL_PAGES = {
    "dl-01": (
        "1. Introduction to Deep Learning",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">1. Introduction to Deep Learning</span>',
        "",
    ),
    "dl-02": (
        "2. The Perceptron",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">2. The Perceptron</span>',
        "",
    ),
    "dl-03": (
        "3. Multi-Layer Perceptron",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">3. Multi-Layer Perceptron</span>',
        "",
    ),
    "dl-04": (
        "4. Forward Propagation",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">4. Forward Propagation</span>',
        "",
    ),
    "dl-05": (
        "5. Loss Functions in Deep Learning",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">5. Loss Functions in Deep Learning</span>',
        "",
    ),
    "dl-11": (
        "11. Convolutional Neural Networks — Fundamentals",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">11. CNN Fundamentals</span>',
        "",
    ),
    "dl-12": (
        "12. CNN — Padding, Strides & Pooling",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">12. Padding, Strides & Pooling</span>',
        "",
    ),
    "dl-13": (
        "13. CNN Architectures & Transfer Learning",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">13. Architectures & Transfer Learning</span>',
        "",
    ),
    "dl-06": (
        "6. Backpropagation",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">6. Backpropagation</span>',
        "",
    ),
    "dl-07": (
        "7. Vanishing & Exploding Gradients",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">7. Vanishing & Exploding Gradients</span>',
        "",
    ),
    "dl-08": (
        "8. Training Deep Networks — Practical Toolkit",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">8. Practical Toolkit</span>',
        "",
    ),
    "dl-09": (
        "9. Activation Functions",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">9. Activation Functions</span>',
        "",
    ),
    "dl-14": (
        "14. Recurrent Neural Networks (RNN)",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">14. RNN</span>',
        "",
    ),
    "dl-15": (
        "15. LSTM & GRU",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">15. LSTM & GRU</span>',
        "",
    ),
    "dl-17": (
        "17. Attention Mechanism",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">17. Attention Mechanism</span>',
        "",
    ),
    "dl-10": (
        "10. Optimizers & Weight Initialization",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">10. Optimizers</span>',
        "",
    ),
    "dl-16": (
        "16. Sequence-to-Sequence & Encoder-Decoder",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">16. Seq2Seq & Encoder-Decoder</span>',
        "",
    ),
    "dl-18": (
        "18. The Transformer Architecture",
        '<a href="../index.html" class="hover:text-[var(--secondary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--secondary)]">DL Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">18. Transformers</span>',
        "",
    ),
}

# page_id -> (title, crumbs_html, extra_js) — NLP track
NLP_PAGES = {
    "nlp-01": (
        "1. Introduction to NLP",
        '<a href="../index.html" class="hover:text-[var(--tertiary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--tertiary)]">NLP Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">1. Introduction to NLP</span>',
        "",
    ),
    "nlp-02": (
        "2. The NLP Pipeline & Text Preprocessing",
        '<a href="../index.html" class="hover:text-[var(--tertiary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--tertiary)]">NLP Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">2. Pipeline & Preprocessing</span>',
        "",
    ),
    "nlp-03": (
        "3. Text Representation",
        '<a href="../index.html" class="hover:text-[var(--tertiary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--tertiary)]">NLP Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">3. Text Representation</span>',
        "",
    ),
    "nlp-04": (
        "4. Word2Vec & Text Classification",
        '<a href="../index.html" class="hover:text-[var(--tertiary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--tertiary)]">NLP Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">4. Word2Vec & Classification</span>',
        "",
    ),
    "nlp-05": (
        "5. Part-of-Speech (POS) Tagging",
        '<a href="../index.html" class="hover:text-[var(--tertiary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--tertiary)]">NLP Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">5. POS Tagging</span>',
        "",
    ),
    "nlp-06": (
        "6. Named Entity Recognition (NER)",
        '<a href="../index.html" class="hover:text-[var(--tertiary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--tertiary)]">NLP Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">6. NER</span>',
        "",
    ),
    "nlp-07": (
        "7. Topic Modeling",
        '<a href="../index.html" class="hover:text-[var(--tertiary)]">Home</a><span class="mx-2">/</span><a href="../index.html#courses" class="hover:text-[var(--tertiary)]">NLP Track</a><span class="mx-2">/</span><span class="text-[var(--on-background)]">7. Topic Modeling</span>',
        "",
    ),
}

if __name__ == "__main__":
    build_home_page()
    for page_id, args in COURSE_PAGES.items():
        build_course_page(page_id, *args, sidebar=SIDEBAR_ML)
    for page_id, args in DL_PAGES.items():
        build_course_page(page_id, *args, sidebar=SIDEBAR_DL)
    for page_id, args in NLP_PAGES.items():
        build_course_page(page_id, *args, sidebar=SIDEBAR_NLP)
