<div align="center">
    
    
 <div>
<!-- 
<a href="https://github.com/Q-Future/"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fvqassessment%2FQ-Bench&count_bg=%23E97EBA&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visitors&edge_flat=false"/></a>
    <a href="https://github.com/Q-Future/Q-Bench"><img src="https://img.shields.io/github/stars/Q-Future/Q-Bench"/></a>
    <a href="https://arxiv.org/abs/2309.14181"><img src="https://img.shields.io/badge/Arxiv-2309:14181-red"/></a>
    <a href="https://arxiv.org/abs/2402.07116"><img src="https://img.shields.io/badge/Extension-2402:07116-yellow"/></a>
    <a href="https://github.com/Q-Future/Q-Bench/releases/tag/v1.0.1.1014datarelease"><img src="https://img.shields.io/badge/Data-Release-green"></a>
    <a href="https://github.com/Q-Future/Q-Instruct"><img src="https://img.shields.io/badge/Awesome-QInstruct-orange"/></a>
   </div> -->


  <h1>OSM+: Cloud-native Open Street Map Data System for City-wide Traffic Experiments</h1>

  <div>
      <a href="https://jhc.sjtu.edu.cn/~gjzheng/" target="_blank">Guanjie Zheng</a><sup>1</sup><sup></sup>,
      <target="_blank">Ziyang Su</a><sup>1</sup><sup></sup>,
      <target="_blank">Yuhang Luo</a><sup>1</sup><sup></sup>,
      <target="_blank">Hongwei Zhang</a><sup>2</sup><sup></sup>,
      
  </div>

<div>
      <target="_blank">Yiheng Wang</a><sup>1</sup><sup></sup>,
      <target="_blank">Linghe Kong</a><sup>1</sup><sup></sup>,
      <target="_blank">Wen Ling</a><sup>1</sup><sup></sup>
  </div>
  <div>
  <sup>1</sup>Shanghai Jiao Tong University, <sup>2</sup>Alibaba Cloud Group
       </div>   
<div>
   </div>
</div>

</div>

### :rocket: Quick Start for OSM+ dataset

1. **Installation.** First, you need to install citybrain-platform package:

```
pip install --upgrade citybrain-platform
```
2. **Platform Register.** Open http://221.228.10.51:18080 in browser and register:

![figure](./assets/citybrain_platform.png "Citybrain Platform")

3. **Get ApiKey.** Click the account name drop-down menu in the upper right corner, click ***Settings*** to enter the personal settings page, and you can view the ApiKey of the current account.

![figure](./assets/apikey.png "Citybrain Platform")

4. **Environment Setting.** Set the CITYBRAIN_APIKEY and BASEURL environment variable before using the library: 

```python
import citybrain_platform

citybrain_platform.api_key = "..."
citybrain_platform.api_baseurl = "http://221.228.10.51:18080/platform/" 
```

5. **Sample Code.**  Our OSM+ dataset is stored as tables, which include:
```
1. osm_node_roadnet
2. osm_fulltag_edge_roadnet
3. osm_split_edge_roadnet
```

you can access these tables using citybrain-platform API:
```python
import citybrain_platform
from citybrain_platform import JobStatus
import time

# Create computing job
job_id = citybrain_platform.Computing.create_job(
  sql="select avg(col_id) from test_tblname;" # SQL commands 
)
print(job_id)

# View the job running status
job_status = citybrain_platform.Computing.get_job_status(
  job_id=job_id # 
)
print(job_status)
while (job_status.status != JobStatus.TERMINATED):
  job_status = citybrain_platform.Computing.get_job_status(job_id=job_id)
  time.sleep(2)
  print(job_status)

# Download result (csv format)
if (job_status.status == JobStatus.TERMINATED):
  citybrain_platform.Computing.get_job_results(
    job_id=job_id, 
    filepath="./results.csv" # Save the result data to the local file path
  )
```

6. **More Information.** For more information about citybrain-platform API, see https://github.com/citybrain-platform/python-library

### Evaluate on Traffic Prediction Task
**If you want to evaluate the OSM+ dataset on traffic prediction task**: We provide a benchmark on 7 baseline methods based on OSM+ and UTD19 datasets. The code is provided in 
[traffic prediction codes](https://github.com/SJTU-CILAB/OSM-dataset/tree/main/code). The following table shows the average performance when horizon = 3,6,12.


<div style="text-align:center">
<table>
	<tr>
      <td></td>
	    <th colspan="2">AGCRN</th>
      <th colspan="2">Crossformer</th>
      <th colspan="2">DCRNN</th>
      <th colspan="2">DLinear</th>
      <th colspan="2">FEDformer</th>
      <th colspan="2">GWNet</th>
      <th colspan="2">MTGNN</th>
  </tr >
    <tr>
        <td>City</td>
        <td>MAE</td>
        <td>MAPE(%)</td>
        <td>MAE</td>
        <td>MAPE(%)</td>
        <td>MAE</td>
        <td>MAPE(%)</td>
        <td>MAE</td>
        <td>MAPE(%)</td>
        <td>MAE</td>
        <td>MAPE(%)</td>
        <td>MAE</td>
        <td>MAPE(%)</td>
        <td>MAE</td>
        <td>MAPE(%)</td>
    </tr>
    <tr>
        <td>AA</td>
        <td>47.92</td>
        <td>44.03</td>
        <th>44.40</th>
        <th>35.34</th>
        <td>OOM</td>
        <td>OOM</td>
        <td>47.80</td>
        <td>37.84</td>
        <td>51.94</td>
        <td>45.19</td>
        <td>47.06</td>
        <td>37.14</td>
        <td>46.97</td>
        <td>40.47</td>
    </tr>
    <tr>
        <td>BSL</td>
        <td>64.51</td>
        <td>55.38</td>
        <td>62.82</td>
        <td>65.68</td>
        <td>119.15</td>
        <td>184.45</td>
        <td>61.50</td>
        <th>51.74</th>
        <th>59.37</th>
        <td>61.78</td>
        <td>81.07</td>
        <td>106.88</td>
        <td>78.41</td>
        <td>93.81</td>
    </tr>
    <tr>
        <td>BRN</td>
        <td>51.00</td>
        <td>231.93</td>
        <th>49.84</th>
        <th>201.84</th>
        <td>OOM</td>
        <td>OOM</td>
        <td>52.18</td>
        <td>253.27</td>
        <td>55.58</td>
        <td>248.00</td>
        <td>50.59</td>
        <td>319.09</td>
        <td>70.90</td>
        <td>405.07</td>
    </tr>
    <tr>
        <td>BHX</td>
        <td>112.08</td>
        <td>70.94</td>
        <th>84.13</th>
        <th>48.08</th>
        <td>303.46</td>
        <td>195.15</td>
        <td>111.22</td>
        <td>66.91</td>
        <td>119.52</td>
        <td>65.15</td>
        <td>107.09</td>
        <td>66.83</td>
        <td>91.68</td>
        <td>49.44</td>
    </tr>
    <tr>
        <td>BOL</td>
        <th>31.27</th>
        <td>21.07</td>
        <td>32.74</td>
        <th>20.98</th>
        <td>38.00</td>
        <td>26.82</td>
        <td>37.27</td>
        <td>34.12</td>
        <td>37.87</td>
        <td>29.83</td>
        <td>35.03</td>
        <td>25.67</td>
        <td>32.31</td>
        <td>21.12</td>
    </tr>
    <tr>
        <td>BOD</td>
        <td>71.65</td>
        <td>39.69</td>
        <td>67.13</td>
        <th>36.19</th>
        <td>232.07</td>
        <td>276.51</td>
        <th>67.13</th>
        <td>44.54</td>
        <td>70.14</td>
        <td>46.29</td>
        <td>74.18</td>
        <td>57.18</td>
        <td>89.14</td>
        <td>56.70</td>
    </tr>
    <tr>
        <td>BRE</td>
        <th>56.31</th>
        <td>36.52</td>
        <td>58.08</td>
        <th>34.22</th>
        <td>OOM</td>
        <td>OOM</td>
        <td>63.27</td>
        <td>42.47</td>
        <td>61.42</td>
        <td>41.98</td>
        <td>57.01</td>
        <td>36.98</td>
        <td>56.69</td>
        <td>35.50</td>
    </tr>
    <tr>
        <td>KN</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>44.78</td>
        <th>48.85</th>
        <td>117.40</td>
        <td>292.38</td>
        <th>38.69</th>
        <td>61.19</td>
        <td>40.98</td>
        <td>67.71</td>
        <td>43.85</td>
        <td>55.18</td>
        <td>47.89</td>
        <td>75.01</td>
    </tr>
    <tr>
        <td>DA</td>
        <td>57.22</td>
        <td>51.76</td>
        <th>53.28</th>
        <td>50.75</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>54.76</td>
        <td>53.99</td>
        <td>57.41</td>
        <td>61.16</td>
        <td>54.69</td>
        <td>51.74</td>
        <td>57.20</td>
        <th>50.30</th>
    </tr>
    <tr>
        <td>ESS</td>
        <td>41.95</td>
        <th>34.65</th>
        <td>40.47</td>
        <td>41.68</td>
        <td>174.64</td>
        <td>294.77</td>
        <td>50.35</td>
        <td>43.85</td>
        <td>44.70</td>
        <td>41.95</td>
        <td>38.99</td>
        <td>34.87</td>
        <th>38.41</th>
        <td>36.46</td>
    </tr>
    <tr>
        <td>FRA</td>
        <td>163.16</td>
        <td>54.95</td>
        <td>145.88</td>
        <td>47.61</td>
        <td>179.03</td>
        <td>51.37</td>
        <th>99.62</th>
        <th>30.19</th>
        <td>107.78</td>
        <td>31.76</td>
        <td>190.85</td>
        <td>62.23</td>
        <td>284.10</td>
        <td>92.89</td>
    </tr>
    <tr>
        <td>GRZ</td>
        <td>61.15</td>
        <td>113.62</td>
        <th>52.78</th>
        <th>66.74</th>
        <td>183.88</td>
        <td>464.62</td>
        <td>60.83</td>
        <td>72.86</td>
        <td>56.16</td>
        <td>73.15</td>
        <td>58.03</td>
        <td>68.32</td>
        <td>56.60</td>
        <td>74.38</td>
    </tr>
    <tr>
        <td>GRQ</td>
        <td>69.64</td>
        <td>35.57</td>
        <td>68.02</td>
        <th>32.53</th>
        <td>158.26</td>
        <td>114.53</td>
        <th>66.03</th>
        <td>37.54</td>
        <td>79.09</td>
        <td>42.20</td>
        <td>67.99</td>
        <td>34.95</td>
        <td>74.99</td>
        <td>39.00</td>
    </tr>
    <tr>
        <td>HAM</td>
        <td>46.50</td>
        <td>44.89</td>
        <td>44.49</td>
        <td>44.87</td>
        <td>97.85</td>
        <td>108.12</td>
        <td>46.69</td>
        <td>49.81</td>
        <td>47.85</td>
        <td>50.69</td>
        <th>44.25</th>
        <th>43.83</th>
        <td>45.02</td>
        <td>44.18</td>
    </tr>
    <tr>
        <td>INN</td>
        <td>72.80</td>
        <td>31.56</td>
        <td>69.28</td>
        <td>37.40</td>
        <td>342.05</td>
        <td>314.50</td>
        <td>89.95</td>
        <td>39.55</td>
        <td>74.44</td>
        <td>32.32</td>
        <th>67.03</th>
        <th>28.53</th>
        <td>OOM</td>
        <td>OOM</td>
    </tr>
    <tr>
        <td>KS</td>
        <td>81.26</td>
        <td>106.06</td>
        <td>86.38</td>
        <td>118.43</td>
        <td>233.90</td>
        <td>427.98</td>
        <td>75.29</td>
        <td>107.43</td>
        <td>89.83</td>
        <td>127.22</td>
        <th>71.23</th>
        <th>94.88</th>
        <td>191.45</td>
        <td>316.68</td>
    </tr>
    <tr>
        <td>MAN</td>
        <td>106.16</td>
        <td>42.54</td>
        <td>97.48</td>
        <td>41.10</td>
        <td>336.42</td>
        <td>280.35</td>
        <td>101.38</td>
        <td>46.21</td>
        <td>110.81</td>
        <td>52.15</td>
        <th>95.91</th>
        <th>38.95</th>
        <td>97.30</td>
        <td>40.74</td>
    </tr>
    <tr>
        <td>MEL</td>
        <td>50.24</td>
        <td>45.88</td>
        <th>45.36</th>
        <td>42.73</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>63.72</td>
        <td>66.55</td>
        <td>53.25</td>
        <td>56.25</td>
        <td>51.91</td>
        <th>36.10</th>
        <td>45.48</td>
        <td>40.26</td>
    </tr>
    <tr>
        <td>RTM</td>
        <th>52.48</th>
        <th>40.29</th>
        <td>53.83</td>
        <td>50.52</td>
        <td>179.76</td>
        <td>347.68</td>
        <td>68.83</td>
        <td>53.19</td>
        <td>68.43</td>
        <td>65.17</td>
        <td>67.03</td>
        <td>50.91</td>
        <td>57.34</td>
        <td>41.07</td>
    </tr>
    <tr>
        <td>SDR</td>
        <td>103.63</td>
        <td>59.74</td>
        <td>102.25</td>
        <td>65.34</td>
        <td>262.60</td>
        <td>271.61</td>
        <td>97.97</td>
        <td>54.70</td>
        <td>125.51</td>
        <td>95.71</td>
        <th>89.36</th>
        <td>47.38</td>
        <td>97.54</td>
        <th>44.61</th>
    </tr>
    <tr>
        <td>SP</td>
        <td>49.08</td>
        <td>39.57</td>
        <th>47.93</th>
        <td>37.74</td>
        <td>119.56</td>
        <td>119.22</td>
        <td>52.95</td>
        <td>45.39</td>
        <td>53.42</td>
        <td>44.88</td>
        <td>48.34</td>
        <td>38.34</td>
        <td>48.05</td>
        <th>37.48</th>
    </tr>
    <tr>
        <td>SXB</td>
        <td>78.34</td>
        <td>39.40</td>
        <td>76.17</td>
        <td>38.72</td>
        <td>261.11</td>
        <td>223.11</td>
        <td>85.62</td>
        <td>46.72</td>
        <td>84.71</td>
        <td>46.10</td>
        <td>76.86</td>
        <td>39.46</td>
        <th>76.01</th>
        <th>37.36</th>
    </tr>
    <tr>
        <td>STR</td>
        <td>58.93</td>
        <td>20.37</td>
        <td>56.60</td>
        <td>19.52</td>
        <td>68.19</td>
        <td>23.30</td>
        <td>65.80</td>
        <td>24.52</td>
        <td>68.38</td>
        <td>23.48</td>
        <th>55.80</th>
        <th>19.05</th>
        <td>OOM</td>
        <td>OOM</td>
    </tr>
    <tr>
        <td>TPE</td>
        <td>136.50</td>
        <td>48.04</td>
        <td>134.51</td>
        <td>48.18</td>
        <td>502.95</td>
        <td>274.25</td>
        <td>142.61</td>
        <td>46.21</td>
        <td>149.12</td>
        <td>53.31</td>
        <th>129.13</th>
        <th>40.14</th>
        <td>130.36</td>
        <td>41.42</td>
    </tr>
    <tr>
        <td>TO</td>
        <td>89.48</td>
        <td>57.66</td>
        <th>81.70</th>
        <th>44.44</th>
        <td>314.62</td>
        <td>390.29</td>
        <td>85.13</td>
        <td>48.01</td>
        <td>87.85</td>
        <td>56.18</td>
        <td>102.69</td>
        <td>60.64</td>
        <td>104.28</td>
        <td>68.82</td>
    </tr>
    <tr>
        <td>YTO</td>
        <td>51.73</td>
        <td>39.35</td>
        <th>51.54</th>
        <td>40.18</td>
        <td>161.46</td>
        <td>145.72</td>
        <td>90.53</td>
        <td>71.76</td>
        <td>62.92</td>
        <td>59.10</td>
        <td>58.04</td>
        <td>38.73</td>
        <td>52.24</td>
        <th>37.42</th>
    </tr>
    <tr>
        <td>TLS</td>
        <td>257.82</td>
        <td>751.49</td>
        <td>255.29</td>
        <td>756.09</td>
        <td>268.70</td>
        <td>847.32</td>
        <td>263.95</td>
        <td>870.21</td>
        <td>296.55</td>
        <td>836.03</td>
        <th>255.26</th>
        <td>751.62</td>
        <td>258.62</td>
        <th>730.09</th>
    </tr>
    <tr>
        <td>UTC</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>50.35</td>
        <td>62.80</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>50.78</td>
        <td>54.42</td>
        <td>66.80</td>
        <td>88.25</td>
        <td>74.98</td>
        <td>88.33</td>
        <th>39.92 </th>
        <th>36.74</th>
    </tr>
    <tr>
        <td>VNO</td>
        <td>88.95</td>
        <td>54.81</td>
        <td>84.09</td>
        <td>49.34</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>76.03</td>
        <td>43.69</td>
        <td>88.84</td>
        <td>49.53</td>
        <th>73.80</th>
        <th>39.27</th>
        <td>96.47</td>
        <td>64.87</td>
    </tr>
    <tr>
        <td>WOB</td>
        <td>54.48</td>
        <td>41.34</td>
        <th>52.21</th>
        <th>39.71</th>
        <td>0.44</td>
        <td>47.61</td>
        <td>62.24</td>
        <td>50.94</td>
        <td>57.60</td>
        <td>50.15</td>
        <td>54.32</td>
        <td>42.30</td>
        <td>53.24</td>
        <td>40.17</td>
    </tr>
    <tr>
        <td>ZRH</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>54.73</td>
        <td>36.93</td>
        <td>OOM</td>
        <td>OOM</td>
        <td>60.36</td>
        <td>43.84</td>
        <td>60.12</td>
        <td>43.74</td>
        <td>66.51</td>
        <td>53.31</td>
        <th>53.52</th>
        <th>35.16</th>
    </tr>
</table>
</div>