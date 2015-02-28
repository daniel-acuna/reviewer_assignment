# Website for Automatic Reviewer Assignment and Manuscript Scoring

*Daniel Acuna<sup>1,2</sup>, Titipat Achakulvisut<sup>2</sup>, Konrad Kording<sup>1,2</sup>*

*<sup>1</sup> Rehabilitation Institute of Chicago*  
*<sup>2</sup> Northwestern University*  

**Keywords:** *Team Assembly, Methods for Science of Team Science Research,
Big Data*


<p>The peer review process is an important component of the scientific process. Its success depends on the right formation of a team of peers that evaluates and scores manuscripts. These steps crucially hinges on editors who must juggle the expertise and conflicts of interests of mostly unknown reviewers, and decide whether to accept the suggested reviewers provided by authors. Recently, however, it has been shown that the peer review process is highly subjective, creating panels that rarely agree among themselves, and biased towards their own domains . Additionally, after the reviews are in, the editors must weigh the scores accounting for potential harshness or carelessness of each reviewer. It is thus important to address these shortcomings to make the review process faster and less biased.
</p>
<table class="image">
<tr><td>
<div style="text-align:center">
<img src="figures/process.png" alt="Title" style="width: 700px;">
</div>
</td></tr>
<caption align="top">
**Figure 1** Reviewer assignment process.
**A.** Article information, reviewer information, and (optionally) conflict of interests beyond co-authorship are combined to produce assignments that maximizes total article-reviewer topic similarity. **B.** Reviewers’ scores are used by a Bayesian random effects model that controls for systematically biased reviewers.
</caption>
</table>
<p>
In this work, we will present a website that implements our current research on automated article-reviewer assignment and manuscript scoring. Importantly, our article-reviewer assignment algorithm provides a good initial solution without using the authors suggested reviewers or reviewers bidding on articles. The algorithm does the matching by finding a global assignment that maximizes the topic similarity between articles and reviewers (Fig 1a). The procedure readily manages conflict of interests due to co-authorship and additional conflict of interests provided by the editors. The assignment is based on an extremely fast topic modeling approach and optimization based on linear programming. Therefore, if needed, the editors can iterate over many automated suggestions made by the system almost in real time. The website, therefore, gives an fast solution to the article-reviewer assignment, which allows editors to focus on the refinement of such assignment and other higher level decisions.
</p>
<table class="image">
<tr><td>
<div style="text-align:center">
<img src="figures/website_screenshot.png" alt="Title" style="width: 500px;">
</div></td>
</tr>
<caption align="bottom">
**Figure 2** Article-reviewer assignment and manuscript scoring website. Freely available at <code>http://pr.scienceofscience.org</code>
</caption>
</table>
<p>
The second algorithm implemented by our website solves the manuscript scoring estimation. The estimation is based on a Bayesian random effects model that automatically control some problems with the naive average scoring per article (Fig. 1b). First, if a reviewer systematically gives higher scores than their peers, the reviewer's scores will have less weigh during the estimation. Second, the scoring system provides uncertainty estimates about each score, potentially signaling which articles are harder to grade. This can be taken into account by editors who would consider external criteria to rank articles and produce accept-reject decisions. This website scoring therefore solves an important problem of the review process and promises to remove biases commonly introduced by editors.
</p>
<p>
This presentation will describe the algorithms and the website to the science of team science audience, emphasizing the growing usage of data to assemble teams. The website and algorithms’ source code are publicly available (Fig. 2) and it is constainly maintained by our laboratory.
</p>
## References
  1. Smith, R. (2006). *Peer review: a flawed process at the heart of science and journals*. Journal of the royal society of medicine, 99(4), 178-182.
  2. Price, Eric (2014). *The NIPS experiment* <code>http://blog.mrtz.org/2014/12/15/the-nips-experiment.html</code> (Visited: 02/26/2015)
  3. van Wilgenburg, E., & Elgar, M. A. (2013). *Confirmation bias in studies of nestmate recognition: a cautionary note for research into the behaviour of animals*. PloS one, 8(1), e53548.
