---
title: "WorkflowHub: Community Framework for Enabling Scientific Workflow Research and Development"
image: /assets/images/news/workflowhub.png
description: Scientific workflows have been almost universally used across scientific domains and have underpinned some of the most significant discoveries of the past several decades. Workflow management systems (WMSs) provide abstraction and automation which enable a broad range of researchers to easily define sophisticated computational processes and to then execute them efficiently on parallel and distributed computing systems. As workflows have been adopted by a number of scientific communities, they are becoming more complex and require more sophisticated workflow management capabilities. A workflow now can analyze terabyte-scale data sets, be composed of one million individual tasks, require coordination between heterogeneous tasks, manage tasks that execute for milliseconds to hours, and can process data streams, files, and data placed in object stores. The computations can be single core workloads, loosely coupled computations, or tightly all within a single workflow, and can run in dispersed computing platforms.
date: 10 April 2020
layout: post
categories:
    - conference
---

The [WorkflowHub project](https://workflowhub.org) is a community framework 
for enabling scientific workflow research and development. It provides foundational 
tools for analyzing workflow execution traces, and generating synthetic, yet 
realistic, workflow traces. These traces can then be used for experimental 
evaluation and development of novel algorithms and systems for overcoming the 
challenge of efficient and robust execution of ever-demanding workflows on 
increasingly complex distributed infrastructures.

The WorkflowHub project uses a [common format](https://workflowhub.org/json-format) 
for representing collected workflow traces and generated synthetic workflows traces. 
Workflow simulators and simulation frameworks that support this common format can 
then use both types of traces interchangeably.

In order to allow users to analyze existing workflow traces and to generate 
synthetic workflow traces, the WorkflowHub framework provides a collection of 
tools released as an [open source Python package](https://workflowhub.readthedocs.io/en/latest/). 
This package provides several tools for analyzing workflow traces. More specifically, 
analyses can be performed to produce statistical summaries of workflow performance 
characteristics, per task type. The WorkflowHub Python package also provides a 
number of workflow recipes for generating realistic synthetic workflow traces. 
The current version of the WorkflowHub's Python package provides recipes for 
generating synthetic workflows for all 6 applications.

Read our [technical report](https://arxiv.org/abs/2009.00250) available at ArXiv.

<iframe src="//www.slideshare.net/slideshow/embed_code/key/ewOXrBdhPDiPPl" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/rafaelsilvajp/workflowhub-community-framework-for-enabling-scientific-workflow-research-and-development" title="WorkflowHub: Community Framework for Enabling Scientific Workflow Research and Development" target="_blank">WorkflowHub: Community Framework for Enabling Scientific Workflow Research and Development</a> </strong> from <strong><a href="https://www.slideshare.net/rafaelsilvajp" target="_blank">Rafael Ferreira da Silva</a></strong> </div>

