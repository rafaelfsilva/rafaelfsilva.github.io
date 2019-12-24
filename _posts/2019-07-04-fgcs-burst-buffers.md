---
title: Measuring the Impact of Burst Buffers on Data-Intensive Scientific Workflows
image: /assets/images/news/fgcsbb2019.png
description: Science applications frequently produce and consume large volumes of data, but delivering this data to and from compute resources can be challenging, as parallel file system performance is not keeping up with compute and memory performance. To mitigate this I/O bottleneck, some systems have deployed burst buffers, but their impact on performance for real-world scientific workflow applications is still not clear. In this paper, we examine the impact of burst buffers through the remote-shared, allocatable burst buffers on the Cori system at NERSC. By running two data-intensive workflows, a high-throughput genome analysis workflow, and a subset of the SCEC high-performance CyberShake workflow, a production seismic hazard analysis workflow, we find that using burst buffers offers read and write improvements of an order of magnitude, and these improvements lead to increased job performance, and thereby increased overall workflow performance, even for long-running CPU-bound jobs.
date: 4 July 2019
layout: post
categories:
    - research-paper
---

Science applications frequently produce and consume large volumes of data, but delivering this data to and from compute resources can be challenging, as parallel file system performance is not keeping up with compute and memory performance. To mitigate this I/O bottleneck, some systems have deployed burst buffers, but their impact on performance for real-world scientific workflow applications is still not clear. In this paper, we examine the impact of burst buffers through the remote-shared, allocatable burst buffers on the Cori system at NERSC. By running two data-intensive workflows, a high-throughput genome analysis workflow, and a subset of the SCEC high-performance CyberShake workflow, a production seismic hazard analysis workflow, we find that using burst buffers offers read and write improvements of an order of magnitude, and these improvements lead to increased job performance, and thereby increased overall workflow performance, even for long-running CPU-bound jobs.

---

**Reference to the paper**

<ul>
                                <li><a href="http://dx.doi.org/10.1016/j.future.2019.06.016" target="_blank" alt="DOI">
                                    <i class="ai ai-doi"></i> </a> <a
                                        href="/files/publications/ferreiradasilva-fgcs-bb-2019.pdf" target="_blank"
                                        alt="PDF"> <i class="far fa-file-pdf"></i> </a> <span
                                        id="ferreiradasilva-fgcs-bb-2019">Ferreira da Silva, R., Callaghan, S., Do, T. M. A., Papadimitriou, G., &amp; Deelman, E. (2019). Measuring the Impact of Burst Buffers on Data-Intensive Scientific Workflows. <i>Future Generation Computer Systems</i>, <i>101</i>, 208–220. https://doi.org/10.1016/j.future.2019.06.016</span>
                                    <br/> <a data-toggle="collapse" href="#bib-ferreiradasilva-fgcs-bb-2019"
                                             role="button" aria-expanded="false"
                                             aria-controls="bib-ferreiradasilva-fgcs-bb-2019" style="color: #999">
                                        [BibTex] </a>
                                    <div class="collapse" id="bib-ferreiradasilva-fgcs-bb-2019">
                                        <figure class="highlight"><pre><code class="language-plain" data-lang="plain">@article{ferreiradasilva-fgcs-bb-2019,
  title = {Measuring the Impact of Burst Buffers on Data-Intensive Scientific Workflows},
  author = {Ferreira da Silva, Rafael and Callaghan, Scott and Do, Tu Mai Anh and Papadimitriou, George and Deelman, Ewa},
  journal = {Future Generation Computer Systems},
  volume = {101},
  number = {},
  pages = {208--220},
  year = {2019},
  doi = {10.1016/j.future.2019.06.016}
}</code></pre>
                                        </figure>
                                    </div>
                                </li>

</ul>