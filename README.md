<div align="center">
    
    
 <div>


  <h1>OSM+: Cloud-native Open Street Map Data System for City-wide Traffic Experiments</h1>

  <!-- <div>
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
   </div> -->
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
      <th></th>
	    <th colspan="2">AGCRN</th>
      <th colspan="2">Crossformer</th>
      <th colspan="2">DCRNN</th>
      <th colspan="2">DLinear</th>
      <th colspan="2">FEDformer</th>
      <th colspan="2">GWNet</th>
      <th colspan="2">MTGNN</th>
  </tr >
    <tr>
        <th>City</th>
        <th>MAE</th>
        <th>MAPE(%)</th>
        <th>MAE</th>
        <th>MAPE(%)</th>
        <th>MAE</th>
        <th>MAPE(%)</th>
        <th>MAE</th>
        <th>MAPE(%)</th>
        <th>MAE</th>
        <th>MAPE(%)</th>
        <th>MAE</th>
        <th>MAPE(%)</th>
        <th>MAE</th>
        <th>MAPE(%)</th>
    </tr>
    <tr>
        <th>AA</th>
        <th>47.92</th>
        <th>44.03</th>
        <th><u>44.40</u></th>
        <th><u>35.34</u></th>
        <th>OOM</th>
        <th>OOM</th>
        <th>47.80</th>
        <th>37.84</th>
        <th>51.94</th>
        <th>45.19</th>
        <th>47.06</th>
        <th>37.14</th>
        <th>46.97</th>
        <th>40.47</th>
    </tr>
    <tr>
        <th>BSL</th>
        <th>64.51</th>
        <th>55.38</th>
        <th>62.82</th>
        <th>65.68</th>
        <th>119.15</th>
        <th>184.45</th>
        <th>61.50</th>
        <th><u>51.74</u></th>
        <th><u>59.37</u></th>
        <th>61.78</th>
        <th>81.07</th>
        <th>106.88</th>
        <th>78.41</th>
        <th>93.81</th>
    </tr>
    <tr>
        <th>BRN</th>
        <th>51.00</th>
        <th>231.93</th>
        <th><u>49.84</u></th>
        <th><u>201.84</u></th>
        <th>OOM</th>
        <th>OOM</th>
        <th>52.18</th>
        <th>253.27</th>
        <th>55.58</th>
        <th>248.00</th>
        <th>50.59</th>
        <th>319.09</th>
        <th>70.90</th>
        <th>405.07</th>
    </tr>
    <tr>
        <th>BHX</th>
        <th>112.08</th>
        <th>70.94</th>
        <th><u>84.13</u></th>
        <th><u>48.08</u></th>
        <th>303.46</th>
        <th>195.15</th>
        <th>111.22</th>
        <th>66.91</th>
        <th>119.52</th>
        <th>65.15</th>
        <th>107.09</th>
        <th>66.83</th>
        <th>91.68</th>
        <th>49.44</th>
    </tr>
    <tr>
        <th>BOL</th>
        <th><u>31.27</u></th>
        <th>21.07</th>
        <th>32.74</th>
        <th><u>20.98</u></th>
        <th>38.00</th>
        <th>26.82</th>
        <th>37.27</th>
        <th>34.12</th>
        <th>37.87</th>
        <th>29.83</th>
        <th>35.03</th>
        <th>25.67</th>
        <th>32.31</th>
        <th>21.12</th>
    </tr>
    <tr>
        <th>BOD</th>
        <th>71.65</th>
        <th>39.69</th>
        <th>67.13</th>
        <th><u>36.19</u></th>
        <th>232.07</th>
        <th>276.51</th>
        <th><u>67.13</u></th>
        <th>44.54</th>
        <th>70.14</th>
        <th>46.29</th>
        <th>74.18</th>
        <th>57.18</th>
        <th>89.14</th>
        <th>56.70</th>
    </tr>
    <tr>
        <th>BRE</th>
        <th><u>56.31</u></th>
        <th>36.52</th>
        <th>58.08</th>
        <th><u>34.22</u></th>
        <th>OOM</th>
        <th>OOM</th>
        <th>63.27</th>
        <th>42.47</th>
        <th>61.42</th>
        <th>41.98</th>
        <th>57.01</th>
        <th>36.98</th>
        <th>56.69</th>
        <th>35.50</th>
    </tr>
    <tr>
        <th>KN</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>44.78</th>
        <th><u>48.85</u></th>
        <th>117.40</th>
        <th>292.38</th>
        <th><u>38.69</u></th>
        <th>61.19</th>
        <th>40.98</th>
        <th>67.71</th>
        <th>43.85</th>
        <th>55.18</th>
        <th>47.89</th>
        <th>75.01</th>
    </tr>
    <tr>
        <th>DA</th>
        <th>57.22</th>
        <th>51.76</th>
        <th><u>53.28</u></th>
        <th>50.75</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>54.76</th>
        <th>53.99</th>
        <th>57.41</th>
        <th>61.16</th>
        <th>54.69</th>
        <th>51.74</th>
        <th>57.20</th>
        <th><u>50.30</u></th>
    </tr>
    <tr>
        <th>ESS</th>
        <th>41.95</th>
        <th><u>34.65</u></th>
        <th>40.47</th>
        <th>41.68</th>
        <th>174.64</th>
        <th>294.77</th>
        <th>50.35</th>
        <th>43.85</th>
        <th>44.70</th>
        <th>41.95</th>
        <th>38.99</th>
        <th>34.87</th>
        <th><u>38.41</u></th>
        <th>36.46</th>
    </tr>
    <tr>
        <th>FRA</th>
        <th>163.16</th>
        <th>54.95</th>
        <th>145.88</th>
        <th>47.61</th>
        <th>179.03</th>
        <th>51.37</th>
        <th><u>99.62</u></th>
        <th><u>30.19</u></th>
        <th>107.78</th>
        <th>31.76</th>
        <th>190.85</th>
        <th>62.23</th>
        <th>284.10</th>
        <th>92.89</th>
    </tr>
    <tr>
        <th>GRZ</th>
        <th>61.15</th>
        <th>113.62</th>
        <th><u>52.78</u></th>
        <th><u>66.74</u></th>
        <th>183.88</th>
        <th>464.62</th>
        <th>60.83</th>
        <th>72.86</th>
        <th>56.16</th>
        <th>73.15</th>
        <th>58.03</th>
        <th>68.32</th>
        <th>56.60</th>
        <th>74.38</th>
    </tr>
    <tr>
        <th>GRQ</th>
        <th>69.64</th>
        <th>35.57</th>
        <th>68.02</th>
        <th><u>32.53</u></th>
        <th>158.26</th>
        <th>114.53</th>
        <th><u>66.03</u></th>
        <th>37.54</th>
        <th>79.09</th>
        <th>42.20</th>
        <th>67.99</th>
        <th>34.95</th>
        <th>74.99</th>
        <th>39.00</th>
    </tr>
    <tr>
        <th>HAM</th>
        <th>46.50</th>
        <th>44.89</th>
        <th>44.49</th>
        <th>44.87</th>
        <th>97.85</th>
        <th>108.12</th>
        <th>46.69</th>
        <th>49.81</th>
        <th>47.85</th>
        <th>50.69</th>
        <th><u>44.25</u></th>
        <th><u>43.83</u></th>
        <th>45.02</th>
        <th>44.18</th>
    </tr>
    <tr>
        <th>INN</th>
        <th>72.80</th>
        <th>31.56</th>
        <th>69.28</th>
        <th>37.40</th>
        <th>342.05</th>
        <th>314.50</th>
        <th>89.95</th>
        <th>39.55</th>
        <th>74.44</th>
        <th>32.32</th>
        <th><u>67.03</u></th>
        <th><u>28.53</u></th>
        <th>OOM</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>KS</th>
        <th>81.26</th>
        <th>106.06</th>
        <th>86.38</th>
        <th>118.43</th>
        <th>233.90</th>
        <th>427.98</th>
        <th>75.29</th>
        <th>107.43</th>
        <th>89.83</th>
        <th>127.22</th>
        <th><u>71.23</u></th>
        <th><u>94.88</u></th>
        <th>191.45</th>
        <th>316.68</th>
    </tr>
    <tr>
        <th>MAN</th>
        <th>106.16</th>
        <th>42.54</th>
        <th>97.48</th>
        <th>41.10</th>
        <th>336.42</th>
        <th>280.35</th>
        <th>101.38</th>
        <th>46.21</th>
        <th>110.81</th>
        <th>52.15</th>
        <th><u>95.91</u></th>
        <th><u>38.95</u></th>
        <th>97.30</th>
        <th>40.74</th>
    </tr>
    <tr>
        <th>MEL</th>
        <th>50.24</th>
        <th>45.88</th>
        <th><u>45.36</u></th>
        <th>42.73</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>63.72</th>
        <th>66.55</th>
        <th>53.25</th>
        <th>56.25</th>
        <th>51.91</th>
        <th><u>36.10</u></th>
        <th>45.48</th>
        <th>40.26</th>
    </tr>
    <tr>
        <th>RTM</th>
        <th><u>52.48</u></th>
        <th><u>40.29</u></th>
        <th>53.83</th>
        <th>50.52</th>
        <th>179.76</th>
        <th>347.68</th>
        <th>68.83</th>
        <th>53.19</th>
        <th>68.43</th>
        <th>65.17</th>
        <th>67.03</th>
        <th>50.91</th>
        <th>57.34</th>
        <th>41.07</th>
    </tr>
    <tr>
        <th>SDR</th>
        <th>103.63</th>
        <th>59.74</th>
        <th>102.25</th>
        <th>65.34</th>
        <th>262.60</th>
        <th>271.61</th>
        <th>97.97</th>
        <th>54.70</th>
        <th>125.51</th>
        <th>95.71</th>
        <th><u>89.36</u></th>
        <th>47.38</th>
        <th>97.54</th>
        <th><u>44.61</u></th>
    </tr>
    <tr>
        <th>SP</th>
        <th>49.08</th>
        <th>39.57</th>
        <th><u>47.93</u></th>
        <th>37.74</th>
        <th>119.56</th>
        <th>119.22</th>
        <th>52.95</th>
        <th>45.39</th>
        <th>53.42</th>
        <th>44.88</th>
        <th>48.34</th>
        <th>38.34</th>
        <th>48.05</th>
        <th><u>37.48</u></th>
    </tr>
    <tr>
        <th>SXB</th>
        <th>78.34</th>
        <th>39.40</th>
        <th>76.17</th>
        <th>38.72</th>
        <th>261.11</th>
        <th>223.11</th>
        <th>85.62</th>
        <th>46.72</th>
        <th>84.71</th>
        <th>46.10</th>
        <th>76.86</th>
        <th>39.46</th>
        <th><u>76.01</u></th>
        <th><u>37.36</u></th>
    </tr>
    <tr>
        <th>STR</th>
        <th>58.93</th>
        <th>20.37</th>
        <th>56.60</th>
        <th>19.52</th>
        <th>68.19</th>
        <th>23.30</th>
        <th>65.80</th>
        <th>24.52</th>
        <th>68.38</th>
        <th>23.48</th>
        <th><u>55.80</u></th>
        <th><u>19.05</u></th>
        <th>OOM</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>TPE</th>
        <th>136.50</th>
        <th>48.04</th>
        <th>134.51</th>
        <th>48.18</th>
        <th>502.95</th>
        <th>274.25</th>
        <th>142.61</th>
        <th>46.21</th>
        <th>149.12</th>
        <th>53.31</th>
        <th><u>129.13</u></th>
        <th><u>40.14</u></th>
        <th>130.36</th>
        <th>41.42</th>
    </tr>
    <tr>
        <th>TO</th>
        <th>89.48</th>
        <th>57.66</th>
        <th><u>81.70</u></th>
        <th><u>44.44</u></th>
        <th>314.62</th>
        <th>390.29</th>
        <th>85.13</th>
        <th>48.01</th>
        <th>87.85</th>
        <th>56.18</th>
        <th>102.69</th>
        <th>60.64</th>
        <th>104.28</th>
        <th>68.82</th>
    </tr>
    <tr>
        <th>YTO</th>
        <th>51.73</th>
        <th>39.35</th>
        <th><u>51.54</u></th>
        <th>40.18</th>
        <th>161.46</th>
        <th>145.72</th>
        <th>90.53</th>
        <th>71.76</th>
        <th>62.92</th>
        <th>59.10</th>
        <th>58.04</th>
        <th>38.73</th>
        <th>52.24</th>
        <th><u>37.42</u></th>
    </tr>
    <tr>
        <th>TLS</th>
        <th>257.82</th>
        <th>751.49</th>
        <th>255.29</th>
        <th>756.09</th>
        <th>268.70</th>
        <th>847.32</th>
        <th>263.95</th>
        <th>870.21</th>
        <th>296.55</th>
        <th>836.03</th>
        <th><u>255.26</u></th>
        <th>751.62</th>
        <th>258.62</th>
        <th><u>730.09</u></th>
    </tr>
    <tr>
        <th>UTC</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>50.35</th>
        <th>62.80</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>50.78</th>
        <th>54.42</th>
        <th>66.80</th>
        <th>88.25</th>
        <th>74.98</th>
        <th>88.33</th>
        <th><u>39.92 </u></th>
        <th><u>36.74</u></th>
    </tr>
    <tr>
        <th>VNO</th>
        <th>88.95</th>
        <th>54.81</th>
        <th>84.09</th>
        <th>49.34</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>76.03</th>
        <th>43.69</th>
        <th>88.84</th>
        <th>49.53</th>
        <th><u>73.80</u></th>
        <th><u>39.27</u></th>
        <th>96.47</th>
        <th>64.87</th>
    </tr>
    <tr>
        <th>WOB</th>
        <th>54.48</th>
        <th>41.34</th>
        <th><u>52.21</u></th>
        <th><u>39.71</u></th>
        <th>0.44</th>
        <th>47.61</th>
        <th>62.24</th>
        <th>50.94</th>
        <th>57.60</th>
        <th>50.15</th>
        <th>54.32</th>
        <th>42.30</th>
        <th>53.24</th>
        <th>40.17</th>
    </tr>
    <tr>
        <th>ZRH</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>54.73</th>
        <th>36.93</th>
        <th>OOM</th>
        <th>OOM</th>
        <th>60.36</th>
        <th>43.84</th>
        <th>60.12</th>
        <th>43.74</th>
        <th>66.51</th>
        <th>53.31</th>
        <th><u>53.52</u></th>
        <th><u>35.16</u></th>
    </tr>
</table>

</div>

The performance comparison for seven baseline methods over 31 real-world city datasets with horizon=3. The best results in each row are underlined. All experiments are repeated five times, and the mean and standard deviation are reported.
<table>
    <tr>
        <th>City</th>
        <th>Metric</th>
        <th>AGCRN</th>
        <th>Crossformer</th>
        <th>DCRNN</th>
        <th>DLinear</th>
        <th>FEDformer</th>
        <th>GWNet</th>
        <th>MTGNN</th>
    </tr>
    <tr>
        <th rowspan="3">AA</th>
        <th>MAE</th>
        <th>42.53 &plusmn 0.22</th>
        <th><u>39.89 &plusmn 0.11</th>
        <th>OOM</th>
        <th>40.56 &plusmn 0.00</th>
        <th>46.15 &plusmn 0.03</th>
        <th>40.65 &plusmn 0.19</th>
        <th>40.76 &plusmn 0.38</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>87.82 &plusmn 0.22</th>
        <th>85.21 &plusmn 0.92</th>
        <th>OOM</th>
        <th>82.00 &plusmn 0.00</th>
        <th>99.68 &plusmn 0.34</th>
        <th><u>81.14 &plusmn 1.17</th>
        <th>83.04 &plusmn 0.33</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>38.97 &plusmn 0.18</th>
        <th><u>31.21 &plusmn 1.72</th>
        <th>OOM</th>
        <th>32.43 &plusmn 0.02</th>
        <th>39.76 &plusmn 0.10</th>
        <th>32.09 &plusmn 0.95</th>
        <th>33.27 &plusmn 2.39</th>
    </tr>
    <tr>
        <th rowspan="3">BSL</th>
        <th>MAE</th>
        <th>55.00 &plusmn 0.15</th>
        <th>49.76 &plusmn 0.96</th>
        <th>116.48 &plusmn 1.50</th>
        <th><u>49.12 &plusmn 0.00</th>
        <th>52.55 &plusmn 0.18</th>
        <th>68.47 &plusmn 0.15</th>
        <th>65.86 &plusmn 0.60</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>82.77 &plusmn 0.08</th>
        <th><u>74.24 &plusmn 2.83</th>
        <th>155.13 &plusmn 0.43</th>
        <th>79.39 &plusmn 0.03</th>
        <th>76.74 &plusmn 0.37</th>
        <th>93.83 &plusmn 1.64</th>
        <th>90.52 &plusmn 1.20</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>45.85 &plusmn 0.35</th>
        <th><u>43.38 &plusmn 2.60</th>
        <th>171.29 &plusmn 7.33</th>
        <th>42.93 &plusmn 0.01</th>
        <th>52.67 &plusmn 1.15</th>
        <th>91.08 &plusmn 3.34</th>
        <th>75.48 &plusmn 2.24</th>
    </tr>
    <tr>
        <th rowspan="3">BRN</th>
        <th>MAE</th>
        <th>46.82 &plusmn 1.30</th>
        <th><u>45.65 &plusmn 0.17</th>
        <th>OOM</th>
        <th>48.76 &plusmn 0.02</th>
        <th>51.16 &plusmn 0.10</th>
        <th>47.49 &plusmn 0.56</th>
        <th>59.36 &plusmn 0.86</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>468.78 &plusmn 9.95</th>
        <th><u>454.56 &plusmn 1.64</th>
        <th>OOM</th>
        <th>454.98 &plusmn 0.18</th>
        <th>431.93 &plusmn 0.45</th>
        <th>440.49 &plusmn 7.76</th>
        <th>477.32 &plusmn 13.68</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>222.50 &plusmn 13.23</th>
        <th>233.32 &plusmn 18.35</th>
        <th>OOM</th>
        <th>229.36 &plusmn 2.05</th>
        <th>232.49 &plusmn 17.64</th>
        <th>278.14 &plusmn 19.92</th>
        <th>347.74 &plusmn 20.37</th>
    </tr>
    <tr>
        <th rowspan="3">BHX</th>
        <th>MAE</th>
        <th>88.84 &plusmn 0.35</th>
        <th>84.86 &plusmn 7.57</th>
        <th>289.70 &plusmn 11.26</th>
        <th>92.86 &plusmn 0.80</th>
        <th>104.66 &plusmn 0.44</th>
        <th>90.95 &plusmn 0.18</th>
        <th><u>84.13 &plusmn 0.64</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>137.05 &plusmn 0.61</th>
        <th>134.05 &plusmn 8.50</th>
        <th>425.16 &plusmn 37.43</th>
        <th>144.99 &plusmn 0.88</th>
        <th>158.84 &plusmn 0.19</th>
        <th>144.59 &plusmn 1.12</th>
        <th><u>130.56 &plusmn 0.88</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>43.38 &plusmn 0.35</th>
        <th><u>40.51 &plusmn 2.58</th>
        <th>191.60 &plusmn 57.29</th>
        <th>48.95 &plusmn 0.11</th>
        <th>52.14 &plusmn 0.90</th>
        <th>51.86 &plusmn 1.83</th>
        <th>45.67 &plusmn 3.76</th>
    </tr>
    <tr>
        <th rowspan="3">BOL</th>
        <th>MAE</th>
        <th><u>29.63 &plusmn 0.27</th>
        <th>32.03 &plusmn 1.73</th>
        <th>32.74 &plusmn 0.38</th>
        <th>33.31 &plusmn 0.02</th>
        <th>34.19 &plusmn 0.04</th>
        <th>32.69 &plusmn 1.92</th>
        <th>29.68 &plusmn 0.23</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>84.46 &plusmn 0.07</th>
        <th>84.23 &plusmn 0.25</th>
        <th>87.89 &plusmn 0.04</th>
        <th>83.81 &plusmn 0.06</th>
        <th>87.51 &plusmn 0.13</th>
        <th>84.37 &plusmn 0.56</th>
        <th><u>81.28 &plusmn 0.13</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>18.44 &plusmn 1.09</th>
        <th>19.69 &plusmn 0.44</th>
        <th>22.48 &plusmn 0.69</th>
        <th>30.71 &plusmn 0.10</th>
        <th>26.86 &plusmn 1.25</th>
        <th>22.51 &plusmn 0.53</th>
        <th>18.63 &plusmn 0.50</th>
    </tr>
    <tr>
        <th rowspan="3">BOD</th>
        <th>MAE</th>
        <th>62.34 &plusmn 0.22</th>
        <th>60.21 &plusmn 0.60</th>
        <th>244.58 &plusmn 20.30</th>
        <th><u>58.23 &plusmn 0.00</th>
        <th>58.51 &plusmn 0.30</th>
        <th>59.78 &plusmn 0.05</th>
        <th>71.17 &plusmn 1.11</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>100.52 &plusmn 0.47</th>
        <th>95.41 &plusmn 0.16</th>
        <th>324.45 &plusmn 24.77</th>
        <th>92.86 &plusmn 0.01</th>
        <th><u>92.09 &plusmn 0.27</th>
        <th>93.00 &plusmn 0.09</th>
        <th>109.95 &plusmn 2.32</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>37.45 &plusmn 1.21</th>
        <th><u>33.47 &plusmn 0.43</th>
        <th>280.19 &plusmn 14.03</th>
        <th>37.59 &plusmn 0.05</th>
        <th>38.28 &plusmn 0.84</th>
        <th>43.06 &plusmn 0.33</th>
        <th>45.75 &plusmn 0.42</th>
    </tr>
    <tr>
        <th rowspan="3">BRE</th>
        <th>MAE</th>
        <th>55.40 &plusmn 0.02</th>
        <th>56.33 &plusmn 1.40</th>
        <th>OOM</th>
        <th>58.99 &plusmn 0.03</th>
        <th>58.80 &plusmn 0.04</th>
        <th>55.45 &plusmn 0.09</th>
        <th><u>55.18 &plusmn 0.17</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>92.18 &plusmn 0.08</th>
        <th>93.06 &plusmn 1.74</th>
        <th>OOM</th>
        <th>97.06 &plusmn 0.11</th>
        <th>95.33 &plusmn 0.02</th>
        <th><u>91.31 &plusmn 0.11</th>
        <th>91.72 &plusmn 0.48</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>36.08 &plusmn 0.26</th>
        <th><u>33.69 &plusmn 1.66</th>
        <th>OOM</th>
        <th>40.12 &plusmn 0.12</th>
        <th>40.41 &plusmn 0.49</th>
        <th>36.10 &plusmn 0.27</th>
        <th>34.93 &plusmn 0.22</th>
    </tr>
    <tr>
        <th rowspan="3">KN</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>39.17 &plusmn 1.36</th>
        <th>119.00 &plusmn 0.09</th>
        <th><u>35.47 &plusmn 0.00</th>
        <th>38.35 &plusmn 0.37</th>
        <th>37.55 &plusmn 0.55</th>
        <th>40.06 &plusmn 0.38</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>62.75 &plusmn 2.15</th>
        <th>152.84 &plusmn 0.67</th>
        <th><u>54.99 &plusmn 0.00</th>
        <th>58.78 &plusmn 0.32</th>
        <th>58.21 &plusmn 0.67</th>
        <th>61.15 &plusmn 0.86</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th>47.64 &plusmn 0.56</th>
        <th>293.93 &plusmn 0.88</th>
        <th>54.02 &plusmn 0.17</th>
        <th>61.77 &plusmn 1.36</th>
        <th><u>47.54 &plusmn 0.59</th>
        <th>58.71 &plusmn 1.08</th>
    </tr>
    <tr>
        <th rowspan="3">DA</th>
        <th>MAE</th>
        <th>56.32 &plusmn 0.04</th>
        <th>51.12 &plusmn 0.79</th>
        <th>OOM</th>
        <th><u>50.77 &plusmn 0.00</th>
        <th>54.26 &plusmn 0.08</th>
        <th>51.80 &plusmn 0.11</th>
        <th>54.58 &plusmn 0.23</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>88.65 &plusmn 0.20</th>
        <th>77.01 &plusmn 1.12</th>
        <th>OOM</th>
        <th><u>75.41 &plusmn 0.00</th>
        <th>79.78 &plusmn 0.25</th>
        <th>78.39 &plusmn 0.16</th>
        <th>86.54 &plusmn 1.08</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>50.79 &plusmn 0.00</th>
        <th><u>45.51 &plusmn 0.49</th>
        <th>OOM</th>
        <th>51.38 &plusmn 0.02</th>
        <th>58.16 &plusmn 0.89</th>
        <th>48.27 &plusmn 0.64</th>
        <th>48.10 &plusmn 0.11</th>
    </tr>
    <tr>
        <th rowspan="3">ESS</th>
        <th>MAE</th>
        <th>40.66 &plusmn 0.28</th>
        <th>36.95 &plusmn 0.10</th>
        <th>172.66 &plusmn 0.19</th>
        <th>41.06 &plusmn 0.00</th>
        <th>40.51 &plusmn 0.07</th>
        <th>36.86 &plusmn 0.08</th>
        <th><u>35.94 &plusmn 0.07</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>59.07 &plusmn 0.76</th>
        <th>53.29 &plusmn 0.27</th>
        <th>224.47 &plusmn 3.72</th>
        <th>59.39 &plusmn 0.01</th>
        <th>58.41 &plusmn 0.03</th>
        <th>53.72 &plusmn 0.22</th>
        <th><u>52.57 &plusmn 0.03</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>35.54 &plusmn 1.10</th>
        <th>34.79 &plusmn 1.28</th>
        <th>302.81 &plusmn 15.18</th>
        <th>34.62 &plusmn 0.40</th>
        <th>36.01 &plusmn 0.71</th>
        <th>32.85 &plusmn 0.28</th>
        <th><u>31.51 &plusmn 2.29</th>
    </tr>
    <tr>
        <th rowspan="3">FRA</th>
        <th>MAE</th>
        <th>124.69 &plusmn 0.05</th>
        <th>140.18 &plusmn 14.57</th>
        <th>185.87 &plusmn 2.29</th>
        <th><u>71.58 &plusmn 0.30</th>
        <th>84.83 &plusmn 1.13</th>
        <th>139.06 &plusmn 1.84</th>
        <th>170.44 &plusmn 12.29</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>157.09 &plusmn 0.09</th>
        <th>166.53 &plusmn 16.07</th>
        <th>237.20 &plusmn 2.82</th>
        <th><u>90.90 &plusmn 1.09</th>
        <th>108.23 &plusmn 2.00</th>
        <th>163.25 &plusmn 2.09</th>
        <th>190.32 &plusmn 12.38</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>39.40 &plusmn 0.02</th>
        <th>41.18 &plusmn 3.19</th>
        <th>47.65 &plusmn 0.59</th>
        <th><u>20.21 &plusmn 0.07</th>
        <th>23.41 &plusmn 0.15</th>
        <th>42.48 &plusmn 0.68</th>
        <th>51.70 &plusmn 3.62</th>
    </tr>
    <tr>
        <th rowspan="3">GRZ</th>
        <th>MAE</th>
        <th>59.06 &plusmn 0.02</th>
        <th><u>50.55 &plusmn 1.02</th>
        <th>174.96 &plusmn 0.00</th>
        <th>52.27 &plusmn 0.00</th>
        <th>50.95 &plusmn 0.24</th>
        <th>55.07 &plusmn 0.74</th>
        <th>53.48 &plusmn 0.62</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>89.07 &plusmn 0.02</th>
        <th>74.28 &plusmn 0.84</th>
        <th>220.49 &plusmn 0.00</th>
        <th>75.95 &plusmn 0.01</th>
        <th><u>74.23 &plusmn 0.17</th>
        <th>81.10 &plusmn 1.00</th>
        <th>82.35 &plusmn 1.49</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>116.57 &plusmn 0.80</th>
        <th>68.30 &plusmn 4.29</th>
        <th>467.17 &plusmn 0.00</th>
        <th><u>63.68 &plusmn 0.15</th>
        <th>66.96 &plusmn 2.12</th>
        <th>68.11 &plusmn 1.24</th>
        <th>71.41 &plusmn 0.40</th>
    </tr>
    <tr>
        <th rowspan="3">GRQ</th>
        <th>MAE</th>
        <th>63.24 &plusmn 0.01</th>
        <th>62.25 &plusmn 1.53</th>
        <th>162.87 &plusmn 0.00</th>
        <th><u>60.08 &plusmn 0.41</th>
        <th>72.11 &plusmn 1.47</th>
        <th>64.33 &plusmn 0.16</th>
        <th>63.21 &plusmn 1.50</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>87.02 &plusmn 0.08</th>
        <th>86.03 &plusmn 0.07</th>
        <th>218.69 &plusmn 0.00</th>
        <th><u>82.72 &plusmn 0.56</th>
        <th>99.96 &plusmn 1.73</th>
        <th>88.41 &plusmn 0.03</th>
        <th>86.27 &plusmn 1.51</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>30.46 &plusmn 0.19</th>
        <th><u>28.82 &plusmn 0.24</th>
        <th>112.24 &plusmn 0.00</th>
        <th>31.41 &plusmn 0.29</th>
        <th>36.83 &plusmn 0.57</th>
        <th>31.79 &plusmn 0.19</th>
        <th>30.87 &plusmn 1.08</th>
    </tr>
    <tr>
        <th rowspan="3">HAM</th>
        <th>MAE</th>
        <th>45.68 &plusmn 0.09</th>
        <th>43.50 &plusmn 0.10</th>
        <th>97.51 &plusmn 0.56</th>
        <th>44.82 &plusmn 0.00</th>
        <th>46.34 &plusmn 0.05</th>
        <th><u>43.28 &plusmn 0.01</th>
        <th>44.05 &plusmn 0.09</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>75.36 &plusmn 0.60</th>
        <th>70.76 &plusmn 0.19</th>
        <th>150.67 &plusmn 2.84</th>
        <th>73.13 &plusmn 0.01</th>
        <th>74.96 &plusmn 0.18</th>
        <th><u>70.69 &plusmn 0.07</th>
        <th>73.02 &plusmn 0.19</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>44.67 &plusmn 0.36</th>
        <th><u>42.79 &plusmn 0.51</th>
        <th>111.42 &plusmn 5.09</th>
        <th>47.93 &plusmn 0.10</th>
        <th>48.93 &plusmn 0.17</th>
        <th>43.48 &plusmn 0.16</th>
        <th>43.30 &plusmn 0.13</th>
    </tr>
    <tr>
        <th rowspan="3">INN</th>
        <th>MAE</th>
        <th>70.05 &plusmn 0.15</th>
        <th>67.34 &plusmn 1.24</th>
        <th>333.14 &plusmn 2.31</th>
        <th>76.43 &plusmn 0.01</th>
        <th>70.66 &plusmn 0.65</th>
        <th><u>65.65 &plusmn 0.12</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>101.84 &plusmn 0.05</th>
        <th>97.03 &plusmn 0.57</th>
        <th>443.91 &plusmn 2.79</th>
        <th>113.93 &plusmn 0.09</th>
        <th>102.62 &plusmn 0.80</th>
        <th><u>95.28 &plusmn 0.17</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>31.38 &plusmn 0.83</th>
        <th>35.24 &plusmn 5.44</th>
        <th>304.36 &plusmn 0.76</th>
        <th>33.84 &plusmn 0.45</th>
        <th>30.70 &plusmn 0.10</th>
        <th><u>28.00 &plusmn 0.42</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th rowspan="3">KS</th>
        <th>MAE</th>
        <th>69.88 &plusmn 0.37</th>
        <th>73.22 &plusmn 1.27</th>
        <th>244.28 &plusmn 0.00</th>
        <th><u>63.22 &plusmn 2.52</th>
        <th>80.77 &plusmn 0.65</th>
        <th>63.34 &plusmn 1.06</th>
        <th>154.46 &plusmn 1.90</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>203.93 &plusmn 0.33</th>
        <th>204.17 &plusmn 2.19</th>
        <th>342.80 &plusmn 0.00</th>
        <th>158.72 &plusmn 4.21</th>
        <th>177.02 &plusmn 0.31</th>
        <th><u>155.08 &plusmn 0.53</th>
        <th>233.89 &plusmn 3.73</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>80.45 &plusmn 1.04</th>
        <th>87.42 &plusmn 3.53</th>
        <th>440.12 &plusmn 0.00</th>
        <th>81.40 &plusmn 4.85</th>
        <th>105.62 &plusmn 1.65</th>
        <th>81.47 &plusmn 2.36</th>
        <th>235.91 &plusmn 0.42</th>
    </tr>
    <tr>
        <th rowspan="3">MAN</th>
        <th>MAE</th>
        <th>97.96 &plusmn 0.71</th>
        <th>87.80 &plusmn 0.65</th>
        <th>336.72 &plusmn 0.00</th>
        <th>92.36 &plusmn 5.65</th>
        <th>99.05 &plusmn 1.29</th>
        <th><u>84.26 &plusmn 0.20</th>
        <th>85.24 &plusmn 0.93</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>169.67 &plusmn 0.73</th>
        <th>160.48 &plusmn 1.62</th>
        <th>448.89 &plusmn 0.00</th>
        <th>156.98 &plusmn 7.85</th>
        <th>167.30 &plusmn 2.46</th>
        <th><u>151.48 &plusmn 0.49</th>
        <th>154.15 &plusmn 2.57</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>39.66 &plusmn 1.35</th>
        <th>37.73 &plusmn 0.54</th>
        <th>283.06 &plusmn 0.00</th>
        <th>42.24 &plusmn 2.20</th>
        <th>46.21 &plusmn 1.60</th>
        <th><u>32.83 &plusmn 0.26</th>
        <th>36.21 &plusmn 1.39</th>
    </tr>
    <tr>
        <th rowspan="3">MEL</th>
        <th>MAE</th>
        <th>37.39 &plusmn 0.00</th>
        <th>36.21 &plusmn 0.95</th>
        <th>OOM</th>
        <th>42.57 &plusmn 0.85</th>
        <th>40.80 &plusmn 0.58</th>
        <th>36.26 &plusmn 0.01</th>
        <th><u>35.86 &plusmn 0.95</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>56.63 &plusmn 0.01</th>
        <th><u>54.30 &plusmn 2.21</th>
        <th>OOM</th>
        <th>64.49 &plusmn 1.03</th>
        <th>60.80 &plusmn 1.36</th>
        <th>54.35 &plusmn 0.06</th>
        <th>54.78 &plusmn 1.68</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>37.60 &plusmn 0.03</th>
        <th>35.63 &plusmn 0.72</th>
        <th>OOM</th>
        <th>37.82 &plusmn 0.99</th>
        <th>43.56 &plusmn 0.04</th>
        <th><u>27.22 &plusmn 0.07</th>
        <th>31.77 &plusmn 0.80</th>
    </tr>
    <tr>
        <th rowspan="3">RTM</th>
        <th>MAE</th>
        <th><u>49.08 &plusmn 0.16</th>
        <th>50.46 &plusmn 0.06</th>
        <th>170.03 &plusmn 0.00</th>
        <th>55.93 &plusmn 0.01</th>
        <th>58.45 &plusmn 0.73</th>
        <th>54.45 &plusmn 0.28</th>
        <th>51.45 &plusmn 0.08</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th><u>87.20 &plusmn 0.12</th>
        <th>87.80 &plusmn 0.13</th>
        <th>232.29 &plusmn 0.00</th>
        <th>95.05 &plusmn 0.02</th>
        <th>96.26 &plusmn 0.90</th>
        <th>92.68 &plusmn 0.52</th>
        <th>88.92 &plusmn 0.36</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>36.76 &plusmn 0.05</th>
        <th>41.26 &plusmn 0.01</th>
        <th>320.02 &plusmn 0.00</th>
        <th>44.61 &plusmn 0.19</th>
        <th>57.44 &plusmn 1.81</th>
        <th>43.72 &plusmn 1.04</th>
        <th>38.46 &plusmn 1.26</th>
    </tr>
    <tr>
        <th rowspan="3">SDR</th>
        <th>MAE</th>
        <th>88.07 &plusmn 0.25</th>
        <th>86.61 &plusmn 1.76</th>
        <th>259.05 &plusmn 0.00</th>
        <th>80.68 &plusmn 0.02</th>
        <th>107.62 &plusmn 1.33</th>
        <th><u>77.84 &plusmn 0.41</th>
        <th>78.50 &plusmn 2.26</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>230.51 &plusmn 0.94</th>
        <th>231.19 &plusmn 0.49</th>
        <th>434.97 &plusmn 0.00</th>
        <th><u>187.89 &plusmn 0.01</th>
        <th>216.83 &plusmn 2.05</th>
        <th>202.47 &plusmn 1.86</th>
        <th>211.89 &plusmn 0.85</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>54.00 &plusmn 1.15</th>
        <th>53.10 &plusmn 6.85</th>
        <th>257.82 &plusmn 0.00</th>
        <th>43.89 &plusmn 0.16</th>
        <th>81.61 &plusmn 0.53</th>
        <th>44.22 &plusmn 3.89</th>
        <th><u>36.34 &plusmn 0.17</th>
    </tr>
    <tr>
        <th rowspan="3">SP</th>
        <th>MAE</th>
        <th>48.92 &plusmn 0.05</th>
        <th><u>47.51 &plusmn 0.03</th>
        <th>121.12 &plusmn 2.04</th>
        <th>50.74 &plusmn 0.01</th>
        <th>52.37 &plusmn 0.11</th>
        <th>47.84 &plusmn 0.05</th>
        <th>47.75 &plusmn 0.11</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>70.45 &plusmn 0.06</th>
        <th><u>68.34 &plusmn 0.07</th>
        <th>172.55 &plusmn 9.56</th>
        <th>72.60 &plusmn 0.06</th>
        <th>74.68 &plusmn 0.06</th>
        <th>68.91 &plusmn 0.17</th>
        <th>68.90 &plusmn 0.02</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>39.84 &plusmn 0.53</th>
        <th><u>36.77 &plusmn 0.11</th>
        <th>102.07 &plusmn 25.06</th>
        <th>43.49 &plusmn 0.00</th>
        <th>43.79 &plusmn 0.59</th>
        <th>37.92 &plusmn 0.33</th>
        <th>37.04 &plusmn 0.13</th>
    </tr>
    <tr>
        <th rowspan="3">SXB</th>
        <th>MAE</th>
        <th>76.69 &plusmn 0.07</th>
        <th>73.93 &plusmn 0.14</th>
        <th>259.67 &plusmn 0.00</th>
        <th>78.84 &plusmn 0.05</th>
        <th>80.54 &plusmn 0.24</th>
        <th>74.23 &plusmn 0.03</th>
        <th><u>73.87 &plusmn 0.41</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>134.85 &plusmn 0.14</th>
        <th><u>130.71 &plusmn 0.32</th>
        <th>360.44 &plusmn 0.00</th>
        <th>138.48 &plusmn 0.03</th>
        <th>141.88 &plusmn 0.15</th>
        <th>131.69 &plusmn 0.05</th>
        <th>131.14 &plusmn 0.23</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>40.04 &plusmn 1.09</th>
        <th>40.73 &plusmn 2.09</th>
        <th>223.03 &plusmn 0.00</th>
        <th>43.50 &plusmn 0.18</th>
        <th>43.51 &plusmn 0.74</th>
        <th>37.64 &plusmn 0.26</th>
        <th><u>36.53 &plusmn 0.63</th>
    </tr>
    <tr>
        <th rowspan="3">STR</th>
        <th>MAE</th>
        <th>57.40 &plusmn 0.43</th>
        <th>57.84 &plusmn 3.60</th>
        <th>59.86 &plusmn 1.67</th>
        <th>60.07 &plusmn 0.08</th>
        <th>68.33 &plusmn 1.18</th>
        <th><u>55.70 &plusmn 0.02</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>74.79 &plusmn 0.28</th>
        <th>75.55 &plusmn 4.24</th>
        <th>78.25 &plusmn 3.02</th>
        <th>78.53 &plusmn 0.16</th>
        <th>89.06 &plusmn 1.27</th>
        <th><u>72.13 &plusmn 0.07</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>18.44 &plusmn 0.08</th>
        <th>19.11 &plusmn 2.18</th>
        <th>19.07 &plusmn 0.70</th>
        <th>20.01 &plusmn 0.01</th>
        <th>22.32 &plusmn 0.45</th>
        <th><u>18.10 &plusmn 0.06</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th rowspan="3">TPE</th>
        <th>MAE</th>
        <th>126.81 &plusmn 0.07</th>
        <th>126.02 &plusmn 3.81</th>
        <th>490.25 &plusmn 8.98</th>
        <th>125.41 &plusmn 0.01</th>
        <th>134.61 &plusmn 0.09</th>
        <th><u>117.30 &plusmn 0.40</th>
        <th>121.00 &plusmn 0.90</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>555.59 &plusmn 1.23</th>
        <th>561.67 &plusmn 10.18</th>
        <th>988.24 &plusmn 11.03</th>
        <th><u>482.59 &plusmn 0.38</th>
        <th>540.48 &plusmn 5.15</th>
        <th>493.02 &plusmn 0.48</th>
        <th>512.90 &plusmn 1.36</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>42.20 &plusmn 0.35</th>
        <th>45.74 &plusmn 5.09</th>
        <th>266.56 &plusmn 4.39</th>
        <th>41.80 &plusmn 0.12</th>
        <th>47.72 &plusmn 0.55</th>
        <th><u>38.30 &plusmn 1.75</th>
        <th>40.01 &plusmn 1.54</th>
    </tr>
    <tr>
        <th rowspan="3">TO</th>
        <th>MAE</th>
        <th>77.75 &plusmn 0.14</th>
        <th>71.06 &plusmn 0.96</th>
        <th>313.88 &plusmn 0.21</th>
        <th><u>68.52 &plusmn 0.01</th>
        <th>74.48 &plusmn 0.07</th>
        <th>74.91 &plusmn 1.05</th>
        <th>80.07 &plusmn 1.05</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>131.86 &plusmn 0.13</th>
        <th>114.97 &plusmn 2.10</th>
        <th>415.51 &plusmn 1.03</th>
        <th><u>111.00 &plusmn 0.07</th>
        <th>118.37 &plusmn 0.35</th>
        <th>116.63 &plusmn 0.82</th>
        <th>124.72 &plusmn 1.31</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>50.86 &plusmn 0.32</th>
        <th><u>39.42 &plusmn 0.29</th>
        <th>400.19 &plusmn 7.19</th>
        <th>40.27 &plusmn 0.47</th>
        <th>48.37 &plusmn 0.98</th>
        <th>46.33 &plusmn 2.97</th>
        <th>52.21 &plusmn 2.04</th>
    </tr>
    <tr>
        <th rowspan="3">YTO</th>
        <th>MAE</th>
        <th>45.81 &plusmn 0.12</th>
        <th>45.25 &plusmn 0.40</th>
        <th>129.55 &plusmn 18.89</th>
        <th>59.49 &plusmn 0.01</th>
        <th>52.16 &plusmn 0.04</th>
        <th>46.68 &plusmn 0.25</th>
        <th><u>44.65 &plusmn 0.07</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>77.29 &plusmn 0.30</th>
        <th><u>74.48 &plusmn 0.06</th>
        <th>192.41 &plusmn 21.36</th>
        <th>95.84 &plusmn 0.09</th>
        <th>81.85 &plusmn 0.04</th>
        <th>77.47 &plusmn 0.47</th>
        <th>75.03 &plusmn 0.00</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>33.49 &plusmn 0.02</th>
        <th><u>32.72 &plusmn 1.55</th>
        <th>114.20 &plusmn 27.77</th>
        <th>42.70 &plusmn 0.66</th>
        <th>46.45 &plusmn 1.69</th>
        <th>35.18 &plusmn 0.38</th>
        <th>33.36 &plusmn 2.07</th>
    </tr>
    <tr>
        <th rowspan="3">TLS</th>
        <th>MAE</th>
        <th>257.32 &plusmn 0.36</th>
        <th><u>255.21 &plusmn 0.28</th>
        <th>264.24 &plusmn 6.15</th>
        <th>263.84 &plusmn 0.00</th>
        <th>296.07 &plusmn 0.02</th>
        <th>255.32 &plusmn 0.00</th>
        <th>259.00 &plusmn 0.03</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>349.78 &plusmn 0.86</th>
        <th>342.51 &plusmn 0.43</th>
        <th>352.70 &plusmn 9.62</th>
        <th>348.15 &plusmn 0.03</th>
        <th>410.70 &plusmn 0.70</th>
        <th><u>341.22 &plusmn 0.34</th>
        <th>349.09 &plusmn 0.86</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>754.88 &plusmn 3.75</th>
        <th>746.38 &plusmn 4.66</th>
        <th>791.79 &plusmn 77.77</th>
        <th>872.83 &plusmn 0.91</th>
        <th>836.22 &plusmn 1.06</th>
        <th>747.55 &plusmn 5.53</th>
        <th><u>726.09 &plusmn 9.80</th>
    </tr>
    <tr>
        <th rowspan="3">UTC</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>51.67 &plusmn 0.80</th>
        <th>OOM</th>
        <th>44.40 &plusmn 1.21</th>
        <th>61.74 &plusmn 1.37</th>
        <th>75.85 &plusmn 0.25</th>
        <th><u>39.61 &plusmn 0.20</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>83.26 &plusmn 3.39</th>
        <th>OOM</th>
        <th>75.24 &plusmn 1.49</th>
        <th>91.06 &plusmn 0.40</th>
        <th>120.97 &plusmn 0.66</th>
        <th><u>68.41 &plusmn 0.37</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th>57.21 &plusmn 15.30</th>
        <th>OOM</th>
        <th>45.37 &plusmn 1.44</th>
        <th>77.81 &plusmn 4.77</th>
        <th>91.81 &plusmn 5.44</th>
        <th><u>37.55 &plusmn 2.65</th>
    </tr>
    <tr>
        <th rowspan="3">VNO</th>
        <th>MAE</th>
        <th>82.75 &plusmn 0.08</th>
        <th>77.98 &plusmn 0.27</th>
        <th>OOM</th>
        <th><u>69.08 &plusmn 1.53</th>
        <th>81.57 &plusmn 0.28</th>
        <th>69.25 &plusmn 0.23</th>
        <th>89.80 &plusmn 1.00</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>112.24 &plusmn 0.29</th>
        <th>106.39 &plusmn 0.56</th>
        <th>OOM</th>
        <th><u>94.18 &plusmn 2.13</th>
        <th>110.65 &plusmn 0.82</th>
        <th>94.42 &plusmn 0.06</th>
        <th>118.34 &plusmn 1.00</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>47.89 &plusmn 0.26</th>
        <th>42.38 &plusmn 0.14</th>
        <th>OOM</th>
        <th>35.59 &plusmn 0.75</th>
        <th>42.38 &plusmn 0.60</th>
        <th><u>35.32 &plusmn 0.81</th>
        <th>57.14 &plusmn 1.75</th>
    </tr>
    <tr>
        <th rowspan="3">WOB</th>
        <th>MAE</th>
        <th>52.66 &plusmn 0.05</th>
        <th>51.73 &plusmn 1.69</th>
        <th>54.51 &plusmn 0.05</th>
        <th>56.05 &plusmn 0.02</th>
        <th>54.89 &plusmn 0.01</th>
        <th>51.27 &plusmn 0.18</th>
        <th><u>51.12 &plusmn 0.01</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>81.81 &plusmn 0.31</th>
        <th>79.60 &plusmn 3.58</th>
        <th>84.03 &plusmn 0.30</th>
        <th>85.65 &plusmn 0.02</th>
        <th>82.31 &plusmn 0.02</th>
        <th><u>78.15 &plusmn 0.24</th>
        <th>78.27 &plusmn 0.04</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>40.76 &plusmn 0.38</th>
        <th><u>37.38 &plusmn 0.17</th>
        <th>42.23 &plusmn 0.24</th>
        <th>46.71 &plusmn 0.06</th>
        <th>46.64 &plusmn 0.10</th>
        <th>39.56 &plusmn 0.58</th>
        <th>39.41 &plusmn 0.80</th>
    </tr>
    <tr>
        <th rowspan="3">ZRH</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>53.23 &plusmn 0.05</th>
        <th>OOM</th>
        <th>56.33 &plusmn 0.00</th>
        <th>56.72 &plusmn 0.08</th>
        <th>59.24 &plusmn 7.75</th>
        <th><u>52.34 &plusmn 0.18</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>75.13 &plusmn 0.05</th>
        <th>OOM</th>
        <th>79.32 &plusmn 0.01</th>
        <th>79.36 &plusmn 0.01</th>
        <th>83.96 &plusmn 11.26</th>
        <th><u>74.05 &plusmn 0.34</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th>35.77 &plusmn 1.18</th>
        <th>OOM</th>
        <th>40.87 &plusmn 0.04</th>
        <th>41.31 &plusmn 0.53</th>
        <th>44.88 &plusmn 11.14</th>
        <th><u>34.95 &plusmn 0.46</th>
    </tr>
</table>

The performance comparison for seven baseline methods over 31 real-world city datasets with horizon=6. The best results in each row are underlined. All experiments are repeated five times, and the mean and standard deviation are reported.
<table>
    <tr>
        <th>City</th>
        <th>Metric</th>
        <th>AGCRN</th>
        <th>Crossformer</th>
        <th>DCRNN</th>
        <th>DLinear</th>
        <th>FEDformer</th>
        <th>GWNet</th>
        <th>MTGNN</th>
    </tr>
    <tr>
        <th rowspan="3">AA</th>
        <th>MAE</th>
        <th>47.27 &plusmn 0.41</th>
        <th><u>43.29 &plusmn 0.11</th>
        <th>OOM</th>
        <th>46.25 &plusmn 0.00</th>
        <th>50.21 &plusmn 0.02</th>
        <th>46.22 &plusmn 0.59</th>
        <th>45.61 &plusmn 0.55</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>100.54 &plusmn 0.22</th>
        <th><u>95.50 &plusmn 1.21</th>
        <th>OOM</th>
        <th>97.90 &plusmn 0.03</th>
        <th>112.57 &plusmn 0.37</th>
        <th>97.17 &plusmn 2.27</th>
        <th>97.30 &plusmn 0.43</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>43.35 &plusmn 0.73</th>
        <th><u>33.68 &plusmn 0.45</th>
        <th>OOM</th>
        <th>36.33 &plusmn 0.15</th>
        <th>42.69 &plusmn 0.09</th>
        <th>36.93 &plusmn 1.56</th>
        <th>37.46 &plusmn 3.09</th>
    </tr>
    <tr>
        <th rowspan="3">BSL</th>
        <th>MAE</th>
        <th>63.95 &plusmn 0.02</th>
        <th>61.81 &plusmn 3.57</th>
        <th>118.10 &plusmn 0.84</th>
        <th><u>59.01 &plusmn 0.01</th>
        <th>59.94 &plusmn 1.42</th>
        <th>81.55 &plusmn 1.76</th>
        <th>78.88 &plusmn 1.13</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>94.86 &plusmn 0.09</th>
        <th>91.78 &plusmn 4.55</th>
        <th>157.37 &plusmn 1.12</th>
        <th>99.52 &plusmn 0.04</th>
        <th><u>87.06 &plusmn 2.86</th>
        <th>114.99 &plusmn 4.41</th>
        <th>110.81 &plusmn 2.49</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>54.81 &plusmn 0.20</th>
        <th>68.11 &plusmn 2.43</th>
        <th>175.12 &plusmn 9.70</th>
        <th><u>49.76 &plusmn 0.16</th>
        <th>59.65 &plusmn 0.08</th>
        <th>109.78 &plusmn 3.98</th>
        <th>91.64 &plusmn 2.08</th>
    </tr>
    <tr>
        <th rowspan="3">BRN</th>
        <th>MAE</th>
        <th>49.20 &plusmn 1.52</th>
        <th><u>48.47 &plusmn 0.32</th>
        <th>OOM</th>
        <th>51.65 &plusmn 0.01</th>
        <th>54.01 &plusmn 0.18</th>
        <th>50.27 &plusmn 0.10</th>
        <th>69.27 &plusmn 0.82</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>481.50 &plusmn 16.19</th>
        <th>465.00 &plusmn 1.10</th>
        <th>OOM</th>
        <th>464.66 &plusmn 0.33</th>
        <th><u>450.70 &plusmn 0.37</th>
        <th>468.88 &plusmn 0.39</th>
        <th>508.09 &plusmn 12.22</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>216.94 &plusmn 6.34</th>
        <th><u>186.02 &plusmn 20.85</th>
        <th>OOM</th>
        <th>244.39 &plusmn 5.93</th>
        <th>242.43 &plusmn 19.54</th>
        <th>293.55 &plusmn 20.22</th>
        <th>411.51 &plusmn 30.03</th>
    </tr>
    <tr>
        <th rowspan="3">BHX</th>
        <th>MAE</th>
        <th>101.87 &plusmn 0.00</th>
        <th><u>86.82 &plusmn 7.11</th>
        <th>299.18 &plusmn 30.69</th>
        <th>103.14 &plusmn 2.28</th>
        <th>113.03 &plusmn 0.16</th>
        <th>99.17 &plusmn 0.39</th>
        <th>89.68 &plusmn 0.34</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>148.33 &plusmn 0.23</th>
        <th><u>133.22 &plusmn 9.67</th>
        <th>426.46 &plusmn 61.57</th>
        <th>156.29 &plusmn 2.41</th>
        <th>175.26 &plusmn 0.51</th>
        <th>150.67 &plusmn 0.76</th>
        <th>137.11 &plusmn 1.22</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>59.01 &plusmn 0.56</th>
        <th><u>45.71 &plusmn 1.30</th>
        <th>229.60 &plusmn 44.64</th>
        <th>57.28 &plusmn 1.81</th>
        <th>57.12 &plusmn 0.60</th>
        <th>56.87 &plusmn 5.04</th>
        <th>49.85 &plusmn 1.96</th>
    </tr>
    <tr>
        <th rowspan="3">BOL</th>
        <th>MAE</th>
        <th><u>30.99 &plusmn 0.09</th>
        <th>32.53 &plusmn 1.31</th>
        <th>37.09 &plusmn 0.61</th>
        <th>35.99 &plusmn 0.07</th>
        <th>35.71 &plusmn 0.38</th>
        <th>33.47 &plusmn 0.60</th>
        <th>31.57 &plusmn 0.32</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>87.74 &plusmn 0.14</th>
        <th>87.00 &plusmn 0.68</th>
        <th>93.43 &plusmn 0.01</th>
        <th>88.23 &plusmn 0.03</th>
        <th>87.93 &plusmn 0.81</th>
        <th>82.40 &plusmn 0.12</th>
        <th><u>82.26 &plusmn 0.01</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>19.58 &plusmn 1.26</th>
        <th>20.30 &plusmn 0.26</th>
        <th>26.38 &plusmn 0.99</th>
        <th>33.56 &plusmn 0.24</th>
        <th>29.66 &plusmn 1.49</th>
        <th>28.79 &plusmn 0.72</th>
        <th>21.63 &plusmn 0.37</th>
    </tr>
    <tr>
        <th rowspan="3">BOD</th>
        <th>MAE</th>
        <th>69.25 &plusmn 0.17</th>
        <th>65.32 &plusmn 0.92</th>
        <th>242.05 &plusmn 12.05</th>
        <th><u>64.43 &plusmn 0.01</th>
        <th>64.68 &plusmn 0.20</th>
        <th>70.55 &plusmn 0.22</th>
        <th>86.45 &plusmn 0.91</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>112.27 &plusmn 0.50</th>
        <th>103.95 &plusmn 0.50</th>
        <th>321.50 &plusmn 16.12</th>
        <th>102.17 &plusmn 0.01</th>
        <th><u>101.21 &plusmn 0.16</th>
        <th>108.43 &plusmn 0.09</th>
        <th>135.49 &plusmn 2.53</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>39.52 &plusmn 1.05</th>
        <th><u>35.61 &plusmn 0.49</th>
        <th>280.80 &plusmn 1.26</th>
        <th>42.14 &plusmn 0.23</th>
        <th>42.19 &plusmn 0.72</th>
        <th>52.86 &plusmn 0.88</th>
        <th>55.08 &plusmn 1.37</th>
    </tr>
    <tr>
        <th rowspan="3">BRE</th>
        <th>MAE</th>
        <th>56.30 &plusmn 0.01</th>
        <th>56.94 &plusmn 0.75</th>
        <th>OOM</th>
        <th>62.32 &plusmn 0.01</th>
        <th>60.38 &plusmn 0.08</th>
        <th>56.86 &plusmn 0.01</th>
        <th><u>56.26 &plusmn 0.27</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>93.86 &plusmn 0.02</th>
        <th>94.36 &plusmn 0.99</th>
        <th>OOM</th>
        <th>101.83 &plusmn 0.07</th>
        <th>97.83 &plusmn 0.11</th>
        <th>93.62 &plusmn 0.02</th>
        <th><u>93.58 &plusmn 0.67</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>36.30 &plusmn 0.14</th>
        <th><u>34.78 &plusmn 0.07</th>
        <th>OOM</th>
        <th>41.95 &plusmn 0.28</th>
        <th>41.36 &plusmn 0.48</th>
        <th>37.02 &plusmn 0.02</th>
        <th>35.45 &plusmn 0.29</th>
    </tr>
    <tr>
        <th rowspan="3">KN</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>43.36 &plusmn 1.67</th>
        <th>118.57 &plusmn 2.65</th>
        <th><u>37.85 &plusmn 0.00</th>
        <th>40.09 &plusmn 0.24</th>
        <th>43.01 &plusmn 1.18</th>
        <th>45.06 &plusmn 0.30</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>69.19 &plusmn 2.16</th>
        <th>151.98 &plusmn 2.99</th>
        <th>61.54 &plusmn 0.01</th>
        <th><u>61.47 &plusmn 0.14</th>
        <th>68.27 &plusmn 1.68</th>
        <th>68.58 &plusmn 0.14</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th><u>47.64 &plusmn 0.45</th>
        <th>294.00 &plusmn 8.92</th>
        <th>59.41 &plusmn 0.17</th>
        <th>64.05 &plusmn 1.65</th>
        <th>53.57 &plusmn 1.58</th>
        <th>68.56 &plusmn 3.07</th>
    </tr>
    <tr>
        <th rowspan="3">DA</th>
        <th>MAE</th>
        <th>58.34 &plusmn 0.14</th>
        <th><u>53.03 &plusmn 0.05</th>
        <th>OOM</th>
        <th>53.93 &plusmn 0.01</th>
        <th>56.35 &plusmn 0.07</th>
        <th>55.08 &plusmn 0.19</th>
        <th>59.16 &plusmn 0.15</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>92.05 &plusmn 0.44</th>
        <th><u>80.86 &plusmn 0.21</th>
        <th>OOM</th>
        <th>81.10 &plusmn 0.07</th>
        <th>83.79 &plusmn 0.23</th>
        <th>84.75 &plusmn 0.59</th>
        <th>96.79 &plusmn 0.57</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>51.28 &plusmn 0.03</th>
        <th><u>47.58 &plusmn 0.26</th>
        <th>OOM</th>
        <th>53.46 &plusmn 0.08</th>
        <th>59.83 &plusmn 0.81</th>
        <th>50.41 &plusmn 1.14</th>
        <th>50.52 &plusmn 0.23</th>
    </tr>
    <tr>
        <th rowspan="3">ESS</th>
        <th>MAE</th>
        <th>41.58 &plusmn 0.11</th>
        <th>39.69 &plusmn 0.44</th>
        <th>173.69 &plusmn 0.75</th>
        <th>47.27 &plusmn 0.00</th>
        <th>43.48 &plusmn 0.01</th>
        <th>38.23 &plusmn 0.14</th>
        <th><u>37.59 &plusmn 0.06</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>61.02 &plusmn 0.33</th>
        <th>57.73 &plusmn 0.93</th>
        <th>226.42 &plusmn 2.28</th>
        <th>68.86 &plusmn 0.02</th>
        <th>63.05 &plusmn 0.26</th>
        <th>56.05 &plusmn 0.23</th>
        <th><u>55.76 &plusmn 0.09</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>34.29 &plusmn 0.34</th>
        <th>40.50 &plusmn 4.51</th>
        <th>299.82 &plusmn 15.01</th>
        <th>40.99 &plusmn 0.15</th>
        <th>39.62 &plusmn 0.40</th>
        <th>34.16 &plusmn 0.17</th>
        <th><u>34.01 &plusmn 2.44</th>
    </tr>
    <tr>
        <th rowspan="3">FRA</th>
        <th>MAE</th>
        <th>158.46 &plusmn 0.09</th>
        <th>141.89 &plusmn 33.64</th>
        <th>187.73 &plusmn 7.77</th>
        <th><u>93.49 &plusmn 1.42</th>
        <th>107.62 &plusmn 2.29</th>
        <th>173.62 &plusmn 3.08</th>
        <th>258.38 &plusmn 13.05</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>192.87 &plusmn 0.02</th>
        <th>172.02 &plusmn 35.30</th>
        <th>236.87 &plusmn 10.11</th>
        <th><u>115.65 &plusmn 1.17</th>
        <th>136.75 &plusmn 3.69</th>
        <th>202.44 &plusmn 2.63</th>
        <th>279.20 &plusmn 13.65</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>52.05 &plusmn 0.01</th>
        <th>43.28 &plusmn 8.91</th>
        <th>52.30 &plusmn 1.53</th>
        <th><u>27.45 &plusmn 0.40</th>
        <th>30.92 &plusmn 0.64</th>
        <th>54.62 &plusmn 1.16</th>
        <th>81.61 &plusmn 3.79</th>
    </tr>
    <tr>
        <th rowspan="3">GRZ</th>
        <th>MAE</th>
        <th>60.79 &plusmn 0.01</th>
        <th><u>52.70 &plusmn 0.96</th>
        <th>185.12 &plusmn 0.00</th>
        <th>58.29 &plusmn 0.01</th>
        <th>54.03 &plusmn 0.24</th>
        <th>58.32 &plusmn 0.87</th>
        <th>56.03 &plusmn 0.20</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>91.77 &plusmn 0.08</th>
        <th><u>77.53 &plusmn 0.71</th>
        <th>233.72 &plusmn 0.00</th>
        <th>84.30 &plusmn 0.04</th>
        <th>78.69 &plusmn 0.12</th>
        <th>86.47 &plusmn 1.17</th>
        <th>87.69 &plusmn 0.61</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>110.69 &plusmn 1.77</th>
        <th><u>65.44 &plusmn 6.48</th>
        <th>465.95 &plusmn 0.00</th>
        <th>72.50 &plusmn 1.27</th>
        <th>69.79 &plusmn 3.62</th>
        <th>71.75 &plusmn 1.36</th>
        <th>72.35 &plusmn 0.12</th>
    </tr>
    <tr>
        <th rowspan="3">GRQ</th>
        <th>MAE</th>
        <th>68.43 &plusmn 0.01</th>
        <th>65.61 &plusmn 1.26</th>
        <th>161.01 &plusmn 0.00</th>
        <th><u>64.78 &plusmn 0.91</th>
        <th>79.46 &plusmn 0.32</th>
        <th>66.49 &plusmn 0.22</th>
        <th>71.04 &plusmn 3.46</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>93.25 &plusmn 0.24</th>
        <th>90.55 &plusmn 0.25</th>
        <th>217.62 &plusmn 0.00</th>
        <th><u>89.18 &plusmn 1.54</th>
        <th>110.72 &plusmn 0.49</th>
        <th>91.41 &plusmn 0.15</th>
        <th>95.64 &plusmn 4.02</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>33.78 &plusmn 0.31</th>
        <th><u>30.45 &plusmn 1.73</th>
        <th>114.12 &plusmn 0.00</th>
        <th>35.59 &plusmn 0.64</th>
        <th>41.81 &plusmn 0.46</th>
        <th>33.33 &plusmn 0.42</th>
        <th>36.21 &plusmn 1.79</th>
    </tr>
    <tr>
        <th rowspan="3">HAM</th>
        <th>MAE</th>
        <th>46.44 &plusmn 0.12</th>
        <th>44.26 &plusmn 0.07</th>
        <th>97.38 &plusmn 0.48</th>
        <th>46.26 &plusmn 0.01</th>
        <th>47.54 &plusmn 0.10</th>
        <th><u>44.16 &plusmn 0.01</th>
        <th>45.04 &plusmn 0.01</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>77.82 &plusmn 0.73</th>
        <th>74.06 &plusmn 0.10</th>
        <th>150.66 &plusmn 2.47</th>
        <th>77.55 &plusmn 0.01</th>
        <th>79.25 &plusmn 0.22</th>
        <th><u>74.06 &plusmn 0.10</th>
        <th>79.08 &plusmn 1.23</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>45.57 &plusmn 0.70</th>
        <th>44.25 &plusmn 2.04</th>
        <th>111.18 &plusmn 3.96</th>
        <th>49.44 &plusmn 0.06</th>
        <th>50.07 &plusmn 0.06</th>
        <th><u>43.68 &plusmn 0.20</th>
        <th>44.06 &plusmn 0.07</th>
    </tr>
    <tr>
        <th rowspan="3">INN</th>
        <th>MAE</th>
        <th>71.83 &plusmn 0.48</th>
        <th>67.78 &plusmn 0.30</th>
        <th>337.43 &plusmn 6.70</th>
        <th>86.47 &plusmn 0.02</th>
        <th>73.73 &plusmn 0.55</th>
        <th><u>66.95 &plusmn 0.28</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>104.72 &plusmn 0.59</th>
        <th>98.77 &plusmn 1.04</th>
        <th>452.25 &plusmn 0.27</th>
        <th>133.76 &plusmn 0.11</th>
        <th>107.19 &plusmn 0.71</th>
        <th><u>97.41 &plusmn 0.45</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>29.79 &plusmn 1.13</th>
        <th>34.04 &plusmn 3.08</th>
        <th>294.18 &plusmn 24.63</th>
        <th>37.85 &plusmn 0.91</th>
        <th>32.08 &plusmn 0.02</th>
        <th><u>28.82 &plusmn 1.09</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th rowspan="3">KS</th>
        <th>MAE</th>
        <th>77.06 &plusmn 0.53</th>
        <th>83.40 &plusmn 5.34</th>
        <th>229.47 &plusmn 0.00</th>
        <th>72.68 &plusmn 1.41</th>
        <th>85.40 &plusmn 0.05</th>
        <th><u>70.79 &plusmn 0.35</th>
        <th>190.66 &plusmn 2.64</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>216.34 &plusmn 0.41</th>
        <th>218.00 &plusmn 4.66</th>
        <th>332.48 &plusmn 0.00</th>
        <th>177.06 &plusmn 2.66</th>
        <th>187.31 &plusmn 0.67</th>
        <th><u>174.04 &plusmn 0.28</th>
        <th>277.37 &plusmn 5.51</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>97.13 &plusmn 1.41</th>
        <th>111.00 &plusmn 17.20</th>
        <th>410.19 &plusmn 0.00</th>
        <th>99.24 &plusmn 1.87</th>
        <th>116.48 &plusmn 0.61</th>
        <th><u>93.42 &plusmn 0.13</th>
        <th>308.03 &plusmn 0.63</th>
    </tr>
    <tr>
        <th rowspan="3">MAN</th>
        <th>MAE</th>
        <th>106.44 &plusmn 1.13</th>
        <th>94.31 &plusmn 0.83</th>
        <th>335.71 &plusmn 0.00</th>
        <th>103.64 &plusmn 10.23</th>
        <th>110.65 &plusmn 0.92</th>
        <th><u>93.95 &plusmn 1.00</th>
        <th>94.68 &plusmn 2.13</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>180.81 &plusmn 1.54</th>
        <th>169.06 &plusmn 0.26</th>
        <th>448.79 &plusmn 0.00</th>
        <th>172.31 &plusmn 13.89</th>
        <th>184.62 &plusmn 2.27</th>
        <th><u>163.00 &plusmn 3.21</th>
        <th>168.90 &plusmn 4.47</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>43.13 &plusmn 1.40</th>
        <th>43.34 &plusmn 2.45</th>
        <th>279.02 &plusmn 0.00</th>
        <th>47.57 &plusmn 4.43</th>
        <th>51.47 &plusmn 0.57</th>
        <th><u>37.68 &plusmn 0.64</th>
        <th>42.02 &plusmn 1.16</th>
    </tr>
    <tr>
        <th rowspan="3">MEL</th>
        <th>MAE</th>
        <th>48.56 &plusmn 0.00</th>
        <th><u>43.98 &plusmn 1.73</th>
        <th>OOM</th>
        <th>58.89 &plusmn 0.02</th>
        <th>50.66 &plusmn 0.49</th>
        <th>49.02 &plusmn 0.20</th>
        <th>46.12 &plusmn 1.29</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>75.34 &plusmn 0.01</th>
        <th><u>66.14 &plusmn 3.55</th>
        <th>OOM</th>
        <th>89.81 &plusmn 0.46</th>
        <th>76.23 &plusmn 0.70</th>
        <th>74.99 &plusmn 0.31</th>
        <th>72.62 &plusmn 2.27</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>44.66 &plusmn 0.05</th>
        <th>40.38 &plusmn 0.06</th>
        <th>OOM</th>
        <th>54.22 &plusmn 0.50</th>
        <th>53.21 &plusmn 0.56</th>
        <th><u>33.97 &plusmn 0.06</th>
        <th>39.97 &plusmn 1.00</th>
    </tr>
    <tr>
        <th rowspan="3">RTM</th>
        <th>MAE</th>
        <th><u>51.36 &plusmn 0.14</th>
        <th>52.84 &plusmn 1.05</th>
        <th>179.34 &plusmn 0.00</th>
        <th>64.94 &plusmn 0.05</th>
        <th>65.13 &plusmn 0.38</th>
        <th>63.44 &plusmn 0.77</th>
        <th>55.79 &plusmn 0.08</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>92.19 &plusmn 0.07</th>
        <th><u>91.97 &plusmn 0.65</th>
        <th>240.67 &plusmn 0.00</th>
        <th>110.95 &plusmn 0.04</th>
        <th>106.66 &plusmn 0.68</th>
        <th>106.73 &plusmn 1.16</th>
        <th>97.29 &plusmn 0.25</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>39.55 &plusmn 0.86</th>
        <th>48.88 &plusmn 3.29</th>
        <th>349.98 &plusmn 0.00</th>
        <th>50.56 &plusmn 0.21</th>
        <th>63.69 &plusmn 0.70</th>
        <th>49.48 &plusmn 0.75</th>
        <th>40.87 &plusmn 1.70</th>
    </tr>
    <tr>
        <th rowspan="3">SDR</th>
        <th>MAE</th>
        <th>101.26 &plusmn 0.42</th>
        <th>98.18 &plusmn 2.76</th>
        <th>256.61 &plusmn 0.00</th>
        <th>93.27 &plusmn 0.06</th>
        <th>119.78 &plusmn 2.36</th>
        <th><u>86.47 &plusmn 0.70</th>
        <th>91.34 &plusmn 2.73</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>252.60 &plusmn 0.01</th>
        <th>249.70 &plusmn 1.91</th>
        <th>433.47 &plusmn 0.00</th>
        <th><u>214.37 &plusmn 0.03</th>
        <th>239.59 &plusmn 2.95</th>
        <th>220.15 &plusmn 1.88</th>
        <th>235.42 &plusmn 0.34</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>58.36 &plusmn 1.09</th>
        <th>52.17 &plusmn 5.47</th>
        <th>255.29 &plusmn 0.00</th>
        <th>51.78 &plusmn 0.42</th>
        <th>89.07 &plusmn 2.29</th>
        <th>49.86 &plusmn 5.91</th>
        <th><u>41.60 &plusmn 0.36</th>
    </tr>
    <tr>
        <th rowspan="3">SP</th>
        <th>MAE</th>
        <th>49.19 &plusmn 0.05</th>
        <th><u>47.78 &plusmn 0.02</th>
        <th>122.39 &plusmn 4.19</th>
        <th>52.40 &plusmn 0.01</th>
        <th>53.30 &plusmn 0.09</th>
        <th>48.28 &plusmn 0.09</th>
        <th>48.06 &plusmn 0.17</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>70.83 &plusmn 0.02</th>
        <th><u>68.35 &plusmn 0.03</th>
        <th>175.09 &plusmn 12.25</th>
        <th>75.17 &plusmn 0.04</th>
        <th>75.91 &plusmn 0.14</th>
        <th>69.62 &plusmn 0.23</th>
        <th>69.28 &plusmn 0.15</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>39.89 &plusmn 0.29</th>
        <th>39.42 &plusmn 0.10</th>
        <th>102.80 &plusmn 22.32</th>
        <th>44.96 &plusmn 0.02</th>
        <th>44.63 &plusmn 0.37</th>
        <th>37.82 &plusmn 0.32</th>
        <th><u>37.33 &plusmn 0.28</th>
    </tr>
    <tr>
        <th rowspan="3">SXB</th>
        <th>MAE</th>
        <th>78.07 &plusmn 0.07</th>
        <th><u>75.86 &plusmn 0.22</th>
        <th>261.26 &plusmn 0.00</th>
        <th>83.83 &plusmn 0.05</th>
        <th>83.48 &plusmn 0.26</th>
        <th>76.43 &plusmn 0.07</th>
        <th>76.10 &plusmn 0.20</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>137.75 &plusmn 0.13</th>
        <th><u>134.97 &plusmn 1.08</th>
        <th>361.96 &plusmn 0.00</th>
        <th>146.93 &plusmn 0.03</th>
        <th>147.22 &plusmn 0.28</th>
        <th>135.84 &plusmn 0.06</th>
        <th>136.00 &plusmn 0.61</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>39.38 &plusmn 0.52</th>
        <th>36.88 &plusmn 0.64</th>
        <th>223.02 &plusmn 0.00</th>
        <th>46.07 &plusmn 0.29</th>
        <th>44.95 &plusmn 0.49</th>
        <th>38.86 &plusmn 0.28</th>
        <th><u>36.87 &plusmn 0.37</th>
    </tr>
    <tr>
        <th rowspan="3">STR</th>
        <th>MAE</th>
        <th>58.31 &plusmn 0.07</th>
        <th>55.90 &plusmn 0.33</th>
        <th>65.43 &plusmn 3.82</th>
        <th>63.52 &plusmn 0.53</th>
        <th>67.70 &plusmn 0.29</th>
        <th><u>55.29 &plusmn 0.12</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>75.53 &plusmn 0.02</th>
        <th>72.34 &plusmn 0.67</th>
        <th>86.65 &plusmn 5.08</th>
        <th>82.43 &plusmn 0.47</th>
        <th>86.71 &plusmn 0.16</th>
        <th><u>71.79 &plusmn 0.33</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>20.16 &plusmn 0.01</th>
        <th><u>18.61 &plusmn 0.29</th>
        <th>21.85 &plusmn 1.88</th>
        <th>22.95 &plusmn 0.11</th>
        <th>24.03 &plusmn 0.61</th>
        <th>18.78 &plusmn 0.04</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th rowspan="3">TPE</th>
        <th>MAE</th>
        <th>134.51 &plusmn 0.20</th>
        <th>130.49 &plusmn 1.84</th>
        <th>509.35 &plusmn 13.02</th>
        <th>138.44 &plusmn 0.00</th>
        <th>144.56 &plusmn 0.25</th>
        <th><u>126.48 &plusmn 0.29</th>
        <th>129.85 &plusmn 0.99</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>604.37 &plusmn 1.42</th>
        <th>606.52 &plusmn 6.88</th>
        <th>1002.98 &plusmn 12.83</th>
        <th>592.89 &plusmn 0.12</th>
        <th>616.55 &plusmn 3.87</th>
        <th><u>567.78 &plusmn 0.27</th>
        <th>589.03 &plusmn 1.28</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>45.86 &plusmn 0.49</th>
        <th>43.77 &plusmn 0.72</th>
        <th>285.05 &plusmn 4.83</th>
        <th>44.76 &plusmn 0.06</th>
        <th>50.48 &plusmn 0.57</th>
        <th><u>40.21 &plusmn 1.83</th>
        <th>41.77 &plusmn 1.29</th>
    </tr>
    <tr>
        <th rowspan="3">TO</th>
        <th>MAE</th>
        <th>87.26 &plusmn 0.28</th>
        <th><u>77.97 &plusmn 0.72</th>
        <th>315.29 &plusmn 0.01</th>
        <th>80.61 &plusmn 0.02</th>
        <th>83.05 &plusmn 0.09</th>
        <th>95.23 &plusmn 1.17</th>
        <th>97.61 &plusmn 0.70</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>149.60 &plusmn 0.47</th>
        <th><u>128.32 &plusmn 1.66</th>
        <th>421.69 &plusmn 3.47</th>
        <th>134.94 &plusmn 0.10</th>
        <th>133.55 &plusmn 0.26</th>
        <th>150.90 &plusmn 1.60</th>
        <th>154.19 &plusmn 0.30</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>55.62 &plusmn 0.22</th>
        <th><u>43.26 &plusmn 0.12</th>
        <th>390.80 &plusmn 15.64</th>
        <th>46.08 &plusmn 0.69</th>
        <th>53.08 &plusmn 1.63</th>
        <th>56.75 &plusmn 2.22</th>
        <th>63.98 &plusmn 1.64</th>
    </tr>
    <tr>
        <th rowspan="3">YTO</th>
        <th>MAE</th>
        <th>52.35 &plusmn 0.07</th>
        <th><u>51.04 &plusmn 0.30</th>
        <th>148.49 &plusmn 17.87</th>
        <th>86.46 &plusmn 0.04</th>
        <th>60.73 &plusmn 0.19</th>
        <th>57.26 &plusmn 0.38</th>
        <th>51.26 &plusmn 0.14</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>88.15 &plusmn 0.01</th>
        <th><u>83.84 &plusmn 0.62</th>
        <th>219.71 &plusmn 22.22</th>
        <th>137.24 &plusmn 0.27</th>
        <th>95.65 &plusmn 0.01</th>
        <th>95.71 &plusmn 0.74</th>
        <th>86.95 &plusmn 0.04</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>38.58 &plusmn 0.02</th>
        <th>37.69 &plusmn 3.84</th>
        <th>110.54 &plusmn 44.26</th>
        <th>65.08 &plusmn 1.92</th>
        <th>53.94 &plusmn 2.03</th>
        <th>37.79 &plusmn 0.83</th>
        <th><u>37.62 &plusmn 1.48</th>
    </tr>
    <tr>
        <th rowspan="3">TLS</th>
        <th>MAE</th>
        <th>257.69 &plusmn 0.41</th>
        <th><u>255.12 &plusmn 0.04</th>
        <th>264.27 &plusmn 6.31</th>
        <th>263.95 &plusmn 0.00</th>
        <th>294.82 &plusmn 0.19</th>
        <th>255.35 &plusmn 0.01</th>
        <th>259.64 &plusmn 0.41</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>350.19 &plusmn 1.23</th>
        <th>342.33 &plusmn 0.54</th>
        <th>352.67 &plusmn 9.87</th>
        <th>348.26 &plusmn 0.09</th>
        <th>408.19 &plusmn 0.21</th>
        <th><u>340.68 &plusmn 0.33</th>
        <th>351.37 &plusmn 2.05</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>761.22 &plusmn 0.81</th>
        <th>745.90 &plusmn 7.41</th>
        <th>792.14 &plusmn 78.55</th>
        <th>869.43 &plusmn 1.90</th>
        <th>833.62 &plusmn 1.57</th>
        <th>749.50 &plusmn 6.72</th>
        <th><u>730.89 &plusmn 9.58</th>
    </tr>
    <tr>
        <th rowspan="3">UTC</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>66.56 &plusmn 26.30</th>
        <th>OOM</th>
        <th>48.87 &plusmn 0.11</th>
        <th>68.00 &plusmn 0.85</th>
        <th>74.93 &plusmn 0.19</th>
        <th><u>40.09 &plusmn 0.10</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>95.10 &plusmn 17.24</th>
        <th>OOM</th>
        <th>83.02 &plusmn 0.25</th>
        <th>99.18 &plusmn 0.36</th>
        <th>122.75 &plusmn 1.30</th>
        <th><u>72.37 &plusmn 0.03</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th>104.15 &plusmn 72.84</th>
        <th>OOM</th>
        <th>51.11 &plusmn 0.40</th>
        <th>90.66 &plusmn 5.26</th>
        <th>89.98 &plusmn 4.19</th>
        <th><u>37.86 &plusmn 3.07</th>
    </tr>
    <tr>
        <th rowspan="3">VNO</th>
        <th>MAE</th>
        <th>87.69 &plusmn 0.14</th>
        <th>83.21 &plusmn 0.40</th>
        <th>OOM</th>
        <th>74.00 &plusmn 1.45</th>
        <th>86.63 &plusmn 0.41</th>
        <th><u>72.98 &plusmn 0.37</th>
        <th>96.27 &plusmn 0.67</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>118.99 &plusmn 0.33</th>
        <th>113.23 &plusmn 0.07</th>
        <th>OOM</th>
        <th>100.58 &plusmn 1.74</th>
        <th>118.15 &plusmn 0.43</th>
        <th><u>99.91 &plusmn 0.11</th>
        <th>127.62 &plusmn 0.73</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>53.52 &plusmn 0.14</th>
        <th>48.97 &plusmn 1.46</th>
        <th>OOM</th>
        <th>41.17 &plusmn 0.65</th>
        <th>46.50 &plusmn 0.59</th>
        <th><u>38.67 &plusmn 1.02</th>
        <th>64.60 &plusmn 1.76</th>
    </tr>
    <tr>
        <th rowspan="3">WOB</th>
        <th>MAE</th>
        <th>53.64 &plusmn 0.29</th>
        <th>54.06 &plusmn 3.31</th>
        <th>58.06 &plusmn 0.03</th>
        <th>61.11 &plusmn 0.00</th>
        <th>56.56 &plusmn 0.08</th>
        <th>53.34 &plusmn 0.36</th>
        <th><u>52.71 &plusmn 0.12</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>84.29 &plusmn 0.58</th>
        <th>83.78 &plusmn 6.06</th>
        <th>91.34 &plusmn 0.32</th>
        <th>95.94 &plusmn 0.02</th>
        <th>85.20 &plusmn 0.03</th>
        <th>82.52 &plusmn 0.55</th>
        <th><u>81.89 &plusmn 0.16</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>40.44 &plusmn 0.19</th>
        <th><u>39.46 &plusmn 1.23</th>
        <th>45.09 &plusmn 0.29</th>
        <th>49.95 &plusmn 0.02</th>
        <th>48.87 &plusmn 0.60</th>
        <th>41.26 &plusmn 0.69</th>
        <th>40.60 &plusmn 1.35</th>
    </tr>
    <tr>
        <th rowspan="3">ZRH</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>54.55 &plusmn 0.39</th>
        <th>OOM</th>
        <th>59.12 &plusmn 0.01</th>
        <th>58.25 &plusmn 0.02</th>
        <th>62.40 &plusmn 10.21</th>
        <th><u>53.08 &plusmn 0.23</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>77.09 &plusmn 0.55</th>
        <th>OOM</th>
        <th>83.71 &plusmn 0.00</th>
        <th>81.89 &plusmn 0.11</th>
        <th>89.30 &plusmn 15.55</th>
        <th><u>75.22 &plusmn 0.44</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th>35.78 &plusmn 2.65</th>
        <th>OOM</th>
        <th>43.08 &plusmn 0.12</th>
        <th>42.26 &plusmn 0.44</th>
        <th>46.00 &plusmn 11.94</th>
        <th><u>35.18 &plusmn 0.34</th>
    </tr>
</table>

The performance comparison for seven baseline methods over 31 real-world city datasets with horizon=12. The best results in each row are underlined. All experiments are repeated five times, and the mean and standard deviation are reported.
<table>
    <tr>
        <th>City</th>
        <th>Metric</th>
        <th>AGCRN</th>
        <th>Crossformer</th>
        <th>DCRNN</th>
        <th>DLinear</th>
        <th>FEDformer</th>
        <th>GWNet</th>
        <th>MTGNN</th>
    </tr>
    <tr>
        <th rowspan="3">AA</th>
        <th>MAE</th>
        <th>55.05 &plusmn 0.93</th>
        <th><u>49.30 &plusmn 0.79</th>
        <th>OOM</th>
        <th>56.58 &plusmn 0.01</th>
        <th>59.64 &plusmn 0.20</th>
        <th>55.81 &plusmn 1.34</th>
        <th>53.30 &plusmn 0.80</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>118.56 &plusmn 0.58</th>
        <th><u>110.08 &plusmn 0.06</th>
        <th>OOM</th>
        <th>122.58 &plusmn 0.10</th>
        <th>132.58 &plusmn 0.19</th>
        <th>117.78 &plusmn 3.74</th>
        <th>115.28 &plusmn 0.52</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>51.73 &plusmn 1.84</th>
        <th><u>41.13 &plusmn 2.19</th>
        <th>OOM</th>
        <th>44.54 &plusmn 0.12</th>
        <th>53.19 &plusmn 0.31</th>
        <th>46.17 &plusmn 2.80</th>
        <th>44.31 &plusmn 3.53</th>
    </tr>
    <tr>
        <th rowspan="3">BSL</th>
        <th>MAE</th>
        <th>74.87 &plusmn 0.54</th>
        <th>81.11 &plusmn 3.35</th>
        <th>120.92 &plusmn 0.42</th>
        <th>76.52 &plusmn 0.22</th>
        <th><u>66.00 &plusmn 0.70</th>
        <th>97.61 &plusmn 4.34</th>
        <th>89.52 &plusmn 0.36</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>110.37 &plusmn 0.82</th>
        <th>122.17 &plusmn 4.15</th>
        <th>160.46 &plusmn 2.57</th>
        <th>126.12 &plusmn 0.48</th>
        <th><u>96.52 &plusmn 0.35</th>
        <th>139.03 &plusmn 8.66</th>
        <th>126.94 &plusmn 0.56</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>65.54 &plusmn 0.65</th>
        <th>89.04 &plusmn 5.12</th>
        <th>183.70 &plusmn 15.83</th>
        <th><u>62.84 &plusmn 0.30</th>
        <th>69.59 &plusmn 3.62</th>
        <th>129.70 &plusmn 6.69</th>
        <th>111.43 &plusmn 0.24</th>
    </tr>
    <tr>
        <th rowspan="3">BRN</th>
        <th>MAE</th>
        <th><u>53.50 &plusmn 2.10</th>
        <th>54.20 &plusmn 1.85</th>
        <th>OOM</th>
        <th>56.13 &plusmn 0.01</th>
        <th>61.14 &plusmn 0.33</th>
        <th>54.13 &plusmn 0.47</th>
        <th>84.36 &plusmn 1.26</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>500.59 &plusmn 21.34</th>
        <th>483.08 &plusmn 0.25</th>
        <th>OOM</th>
        <th>495.21 &plusmn 0.17</th>
        <th>489.57 &plusmn 0.68</th>
        <th><u>479.82 &plusmn 1.60</th>
        <th>553.53 &plusmn 12.87</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>245.52 &plusmn 4.25</th>
        <th><u>202.93 &plusmn 62.89</th>
        <th>OOM</th>
        <th>290.64 &plusmn 1.52</th>
        <th>307.33 &plusmn 16.91</th>
        <th>340.44 &plusmn 23.69</th>
        <th>513.55 &plusmn 31.06</th>
    </tr>
    <tr>
        <th rowspan="3">BHX</th>
        <th>MAE</th>
        <th>146.03 &plusmn 0.35</th>
        <th>102.03 &plusmn 15.50</th>
        <th>282.12 &plusmn 13.73</th>
        <th>131.89 &plusmn 9.65</th>
        <th>140.17 &plusmn 0.70</th>
        <th>129.19 &plusmn 2.55</th>
        <th><u>101.51 &plusmn 0.10</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>208.28 &plusmn 0.65</th>
        <th>155.04 &plusmn 22.46</th>
        <th>384.96 &plusmn 40.10</th>
        <th>193.75 &plusmn 6.56</th>
        <th>214.60 &plusmn 0.16</th>
        <th>192.02 &plusmn 0.76</th>
        <th><u>154.51 &plusmn 0.86</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>109.60 &plusmn 0.28</th>
        <th>63.90 &plusmn 4.44</th>
        <th>279.89 &plusmn 61.60</th>
        <th>90.05 &plusmn 7.98</th>
        <th>86.17 &plusmn 0.27</th>
        <th>80.07 &plusmn 9.65</th>
        <th><u>58.53 &plusmn 2.38</th>
    </tr>
    <tr>
        <th rowspan="3">BOL</th>
        <th>MAE</th>
        <th><u>33.38 &plusmn 0.12</th>
        <th>35.32 &plusmn 0.68</th>
        <th>45.53 &plusmn 0.92</th>
        <th>42.42 &plusmn 0.09</th>
        <th>44.03 &plusmn 0.11</th>
        <th>39.58 &plusmn 2.22</th>
        <th>34.94 &plusmn 0.49</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>93.57 &plusmn 0.67</th>
        <th>93.44 &plusmn 2.09</th>
        <th>106.98 &plusmn 0.01</th>
        <th>102.71 &plusmn 0.26</th>
        <th>105.61 &plusmn 0.31</th>
        <th>97.56 &plusmn 0.15</th>
        <th><u>92.74 &plusmn 0.59</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>23.09 &plusmn 0.63</th>
        <th><u>22.13 &plusmn 0.46</th>
        <th>33.86 &plusmn 1.51</th>
        <th>38.07 &plusmn 0.13</th>
        <th>33.57 &plusmn 0.61</th>
        <th>27.38 &plusmn 1.10</th>
        <th>22.27 &plusmn 0.29</th>
    </tr>
    <tr>
        <th rowspan="3">BOD</th>
        <th>MAE</th>
        <th>84.17 &plusmn 0.76</th>
        <th><u>78.48 &plusmn 2.18</th>
        <th>234.94 &plusmn 3.51</th>
        <th>78.76 &plusmn 0.01</th>
        <th>87.29 &plusmn 0.40</th>
        <th>91.20 &plusmn 1.25</th>
        <th>109.35 &plusmn 1.40</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>138.13 &plusmn 1.65</th>
        <th>125.87 &plusmn 0.23</th>
        <th>312.43 &plusmn 6.74</th>
        <th><u>122.38 &plusmn 0.08</th>
        <th>131.87 &plusmn 0.90</th>
        <th>139.59 &plusmn 1.34</th>
        <th>173.27 &plusmn 0.92</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>44.29 &plusmn 0.82</th>
        <th><u>41.19 &plusmn 1.49</th>
        <th>278.32 &plusmn 1.47</th>
        <th>54.23 &plusmn 0.18</th>
        <th>59.39 &plusmn 0.18</th>
        <th>73.00 &plusmn 2.49</th>
        <th>74.25 &plusmn 5.28</th>
    </tr>
    <tr>
        <th rowspan="3">BRE</th>
        <th>MAE</th>
        <th><u>57.33 &plusmn 0.09</th>
        <th>59.38 &plusmn 0.08</th>
        <th>OOM</th>
        <th>68.48 &plusmn 0.01</th>
        <th>64.98 &plusmn 0.09</th>
        <th>58.62 &plusmn 0.06</th>
        <th>58.05 &plusmn 0.39</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th><u>95.67 &plusmn 0.22</th>
        <th>98.02 &plusmn 0.06</th>
        <th>OOM</th>
        <th>111.31 &plusmn 0.02</th>
        <th>103.81 &plusmn 0.10</th>
        <th>96.37 &plusmn 0.06</th>
        <th>96.10 &plusmn 0.84</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>36.89 &plusmn 0.01</th>
        <th><u>35.19 &plusmn 0.34</th>
        <th>OOM</th>
        <th>45.77 &plusmn 0.22</th>
        <th>44.95 &plusmn 0.13</th>
        <th>38.23 &plusmn 0.29</th>
        <th>36.70 &plusmn 0.29</th>
    </tr>
    <tr>
        <th rowspan="3">KN</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>52.98 &plusmn 1.36</th>
        <th>116.61 &plusmn 0.23</th>
        <th><u>42.78 &plusmn 0.05</th>
        <th>44.75 &plusmn 0.24</th>
        <th>49.44 &plusmn 0.46</th>
        <th>57.22 &plusmn 1.96</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>83.22 &plusmn 0.84</th>
        <th>149.74 &plusmn 0.66</th>
        <th>67.32 &plusmn 0.14</th>
        <th><u>65.83 &plusmn 0.35</th>
        <th>79.03 &plusmn 0.50</th>
        <th>86.98 &plusmn 2.16</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th><u>54.05 &plusmn 3.83</th>
        <th>297.19 &plusmn 1.49</th>
        <th>70.57 &plusmn 0.27</th>
        <th>77.29 &plusmn 3.06</th>
        <th>61.92 &plusmn 1.39</th>
        <th>89.88 &plusmn 6.97</th>
    </tr>
    <tr>
        <th rowspan="3">DA</th>
        <th>MAE</th>
        <th>56.88 &plusmn 0.01</th>
        <th><u>56.19 &plusmn 0.15</th>
        <th>OOM</th>
        <th>59.55 &plusmn 0.01</th>
        <th>61.34 &plusmn 0.24</th>
        <th>57.52 &plusmn 0.40</th>
        <th>57.85 &plusmn 0.09</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>88.16 &plusmn 0.02</th>
        <th><u>86.45 &plusmn 0.70</th>
        <th>OOM</th>
        <th>90.81 &plusmn 0.06</th>
        <th>90.98 &plusmn 0.34</th>
        <th>87.83 &plusmn 1.01</th>
        <th>90.13 &plusmn 0.16</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>53.29 &plusmn 0.09</th>
        <th>54.39 &plusmn 6.00</th>
        <th>OOM</th>
        <th>57.20 &plusmn 0.02</th>
        <th>66.56 &plusmn 0.19</th>
        <th>55.03 &plusmn 0.35</th>
        <th><u>52.07 &plusmn 0.04</th>
    </tr>
    <tr>
        <th rowspan="3">ESS</th>
        <th>MAE</th>
        <th>44.08 &plusmn 0.27</th>
        <th>44.91 &plusmn 0.32</th>
        <th>179.03 &plusmn 1.10</th>
        <th>62.74 &plusmn 0.04</th>
        <th>49.97 &plusmn 0.14</th>
        <th>41.68 &plusmn 0.05</th>
        <th><u>41.42 &plusmn 0.27</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>65.43 &plusmn 0.68</th>
        <th>67.98 &plusmn 0.93</th>
        <th>232.52 &plusmn 0.26</th>
        <th>92.85 &plusmn 0.16</th>
        <th>73.19 &plusmn 0.40</th>
        <th><u>62.40 &plusmn 0.24</th>
        <th>63.04 &plusmn 0.50</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>35.95 &plusmn 1.15</th>
        <th>49.74 &plusmn 5.81</th>
        <th>308.94 &plusmn 8.39</th>
        <th>55.33 &plusmn 1.11</th>
        <th>48.59 &plusmn 1.21</th>
        <th>37.57 &plusmn 0.39</th>
        <th>38.41 &plusmn 2.97</th>
    </tr>
    <tr>
        <th rowspan="3">FRA</th>
        <th>MAE</th>
        <th>205.72 &plusmn 0.83</th>
        <th>205.31 &plusmn 22.15</th>
        <th>168.51 &plusmn 1.59</th>
        <th><u>109.03 &plusmn 36.74</th>
        <th>132.32 &plusmn 1.38</th>
        <th>250.59 &plusmn 11.89</th>
        <th>386.51 &plusmn 26.96</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>238.54 &plusmn 0.79</th>
        <th>234.38 &plusmn 24.27</th>
        <th>209.58 &plusmn 0.03</th>
        <th><u>132.51 &plusmn 38.23</th>
        <th>165.66 &plusmn 0.15</th>
        <th>282.51 &plusmn 11.51</th>
        <th>408.51 &plusmn 27.19</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>73.26 &plusmn 0.25</th>
        <th>70.54 &plusmn 5.11</th>
        <th>55.50 &plusmn 0.97</th>
        <th><u>35.27 &plusmn 11.29</th>
        <th>41.22 &plusmn 0.39</th>
        <th>85.66 &plusmn 5.06</th>
        <th>132.85 &plusmn 10.28</th>
    </tr>
    <tr>
        <th rowspan="3">GRZ</th>
        <th>MAE</th>
        <th>63.46 &plusmn 0.17</th>
        <th><u>57.03 &plusmn 0.76</th>
        <th>191.54 &plusmn 0.00</th>
        <th>71.93 &plusmn 0.01</th>
        <th>63.14 &plusmn 0.03</th>
        <th>62.37 &plusmn 0.78</th>
        <th>59.51 &plusmn 0.28</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>95.67 &plusmn 0.07</th>
        <th><u>83.99 &plusmn 0.61</th>
        <th>241.77 &plusmn 0.00</th>
        <th>103.75 &plusmn 0.01</th>
        <th>91.38 &plusmn 0.00</th>
        <th>92.58 &plusmn 0.82</th>
        <th>95.09 &plusmn 0.61</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>109.30 &plusmn 3.51</th>
        <th>77.93 &plusmn 5.43</th>
        <th>460.74 &plusmn 0.00</th>
        <th>81.48 &plusmn 0.13</th>
        <th>78.44 &plusmn 0.27</th>
        <th><u>70.16 &plusmn 4.58</th>
        <th>77.40 &plusmn 2.29</th>
    </tr>
    <tr>
        <th rowspan="3">GRQ</th>
        <th>MAE</th>
        <th>77.05 &plusmn 0.27</th>
        <th><u>72.08 &plusmn 3.04</th>
        <th>150.91 &plusmn 0.00</th>
        <th>72.34 &plusmn 1.76</th>
        <th>83.37 &plusmn 2.14</th>
        <th>72.33 &plusmn 0.77</th>
        <th>82.93 &plusmn 6.04</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>104.16 &plusmn 0.05</th>
        <th><u>98.38 &plusmn 2.63</th>
        <th>205.49 &plusmn 0.00</th>
        <th>100.03 &plusmn 0.44</th>
        <th>115.72 &plusmn 2.69</th>
        <th>100.25 &plusmn 0.83</th>
        <th>110.28 &plusmn 7.48</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>41.63 &plusmn 0.69</th>
        <th><u>35.60 &plusmn 1.85</th>
        <th>117.24 &plusmn 0.00</th>
        <th>44.18 &plusmn 2.38</th>
        <th>46.94 &plusmn 1.33</th>
        <th>38.69 &plusmn 0.88</th>
        <th>45.80 &plusmn 2.96</th>
    </tr>
    <tr>
        <th rowspan="3">HAM</th>
        <th>MAE</th>
        <th>47.08 &plusmn 0.23</th>
        <th>45.88 &plusmn 0.41</th>
        <th>97.51 &plusmn 0.59</th>
        <th>48.97 &plusmn 0.02</th>
        <th>49.77 &plusmn 0.01</th>
        <th><u>45.35 &plusmn 0.05</th>
        <th>46.06 &plusmn 0.01</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>80.67 &plusmn 0.53</th>
        <th>78.49 &plusmn 1.08</th>
        <th>150.82 &plusmn 2.57</th>
        <th>84.20 &plusmn 0.08</th>
        <th>83.90 &plusmn 0.06</th>
        <th><u>77.70 &plusmn 0.01</th>
        <th>82.77 &plusmn 2.08</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>45.78 &plusmn 0.83</th>
        <th><u>44.31 &plusmn 3.07</th>
        <th>111.41 &plusmn 4.58</th>
        <th>52.32 &plusmn 0.20</th>
        <th>53.06 &plusmn 0.21</th>
        <th>44.81 &plusmn 0.31</th>
        <th>45.29 &plusmn 0.06</th>
    </tr>
    <tr>
        <th rowspan="3">INN</th>
        <th>MAE</th>
        <th>75.51 &plusmn 0.80</th>
        <th>72.05 &plusmn 0.00</th>
        <th>347.11 &plusmn 2.98</th>
        <th>106.94 &plusmn 0.00</th>
        <th>80.50 &plusmn 1.00</th>
        <th><u>69.08 &plusmn 0.43</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>110.87 &plusmn 0.65</th>
        <th>106.99 &plusmn 0.06</th>
        <th>464.48 &plusmn 8.39</th>
        <th>173.49 &plusmn 0.15</th>
        <th>117.77 &plusmn 1.61</th>
        <th><u>100.59 &plusmn 0.79</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>31.27 &plusmn 1.22</th>
        <th>36.38 &plusmn 0.72</th>
        <th>300.48 &plusmn 37.49</th>
        <th>46.75 &plusmn 0.75</th>
        <th>34.23 &plusmn 0.15</th>
        <th><u>27.74 &plusmn 0.06</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th rowspan="3">KS</th>
        <th>MAE</th>
        <th>97.97 &plusmn 0.72</th>
        <th>103.19 &plusmn 5.03</th>
        <th>227.96 &plusmn 0.00</th>
        <th><u>78.86 &plusmn 14.60</th>
        <th>104.59 &plusmn 1.19</th>
        <th>80.04 &plusmn 0.72</th>
        <th>224.87 &plusmn 1.62</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>244.74 &plusmn 0.48</th>
        <th>244.15 &plusmn 6.33</th>
        <th>332.77 &plusmn 0.00</th>
        <th><u>188.64 &plusmn 2.13</th>
        <th>209.20 &plusmn 1.15</th>
        <th>195.69 &plusmn 0.26</th>
        <th>314.80 &plusmn 4.13</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>143.62 &plusmn 1.84</th>
        <th>156.53 &plusmn 13.18</th>
        <th>433.64 &plusmn 0.00</th>
        <th>110.39 &plusmn 41.23</th>
        <th>162.29 &plusmn 2.84</th>
        <th><u>109.72 &plusmn 2.55</th>
        <th>407.04 &plusmn 1.53</th>
    </tr>
    <tr>
        <th rowspan="3">MAN</th>
        <th>MAE</th>
        <th>117.20 &plusmn 2.55</th>
        <th>109.56 &plusmn 2.55</th>
        <th>336.84 &plusmn 0.00</th>
        <th><u>103.86 &plusmn 9.84</th>
        <th>123.20 &plusmn 0.27</th>
        <th>107.88 &plusmn 1.14</th>
        <th>107.97 &plusmn 2.60</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>196.04 &plusmn 4.11</th>
        <th>190.75 &plusmn 4.72</th>
        <th>450.82 &plusmn 0.00</th>
        <th><u>173.23 &plusmn 12.91</th>
        <th>198.08 &plusmn 0.51</th>
        <th>181.98 &plusmn 4.00</th>
        <th>186.65 &plusmn 3.39</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>47.38 &plusmn 0.86</th>
        <th>45.64 &plusmn 2.89</th>
        <th>278.97 &plusmn 0.00</th>
        <th>46.64 &plusmn 3.55</th>
        <th>60.39 &plusmn 0.14</th>
        <th><u>44.84 &plusmn 1.22</th>
        <th>47.02 &plusmn 1.75</th>
    </tr>
    <tr>
        <th rowspan="3">MEL</th>
        <th>MAE</th>
        <th>64.79 &plusmn 0.03</th>
        <th><u>54.63 &plusmn 4.48</th>
        <th>OOM</th>
        <th>87.95 &plusmn 1.60</th>
        <th>67.32 &plusmn 0.31</th>
        <th>69.54 &plusmn 1.08</th>
        <th>56.73 &plusmn 0.94</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>101.09 &plusmn 0.06</th>
        <th><u>81.23 &plusmn 6.52</th>
        <th>OOM</th>
        <th>127.60 &plusmn 1.41</th>
        <th>97.39 &plusmn 0.04</th>
        <th>105.83 &plusmn 1.53</th>
        <th>87.59 &plusmn 0.91</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>55.34 &plusmn 0.02</th>
        <th>49.10 &plusmn 5.14</th>
        <th>OOM</th>
        <th>103.87 &plusmn 4.79</th>
        <th>70.74 &plusmn 1.14</th>
        <th><u>47.17 &plusmn 0.20</th>
        <th>50.21 &plusmn 0.12</th>
    </tr>
    <tr>
        <th rowspan="3">RTM</th>
        <th>MAE</th>
        <th><u>57.11 &plusmn 0.15</th>
        <th>58.08 &plusmn 1.24</th>
        <th>189.90 &plusmn 0.00</th>
        <th>85.30 &plusmn 0.50</th>
        <th>82.23 &plusmn 0.36</th>
        <th>85.20 &plusmn 1.78</th>
        <th>65.01 &plusmn 0.31</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>99.90 &plusmn 0.34</th>
        <th><u>98.98 &plusmn 0.53</th>
        <th>250.70 &plusmn 0.00</th>
        <th>141.23 &plusmn 0.46</th>
        <th>128.17 &plusmn 0.09</th>
        <th>136.93 &plusmn 2.26</th>
        <th>110.64 &plusmn 0.98</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th><u>43.47 &plusmn 0.63</th>
        <th>55.83 &plusmn 11.21</th>
        <th>373.03 &plusmn 0.00</th>
        <th>65.00 &plusmn 0.87</th>
        <th>76.28 &plusmn 0.17</th>
        <th>62.30 &plusmn 2.15</th>
        <th>46.88 &plusmn 1.28</th>
    </tr>
    <tr>
        <th rowspan="3">SDR</th>
        <th>MAE</th>
        <th>121.60 &plusmn 0.24</th>
        <th>129.77 &plusmn 6.53</th>
        <th>272.16 &plusmn 0.00</th>
        <th>120.00 &plusmn 0.03</th>
        <th>152.27 &plusmn 0.77</th>
        <th><u>104.78 &plusmn 0.34</th>
        <th>119.57 &plusmn 0.47</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>278.70 &plusmn 0.41</th>
        <th>279.99 &plusmn 1.64</th>
        <th>440.08 &plusmn 0.00</th>
        <th>262.91 &plusmn 0.01</th>
        <th>284.60 &plusmn 0.05</th>
        <th><u>249.10 &plusmn 0.76</th>
        <th>274.87 &plusmn 3.75</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>67.07 &plusmn 2.54</th>
        <th>92.03 &plusmn 14.14</th>
        <th>301.72 &plusmn 0.00</th>
        <th>68.81 &plusmn 0.28</th>
        <th>119.83 &plusmn 1.98</th>
        <th>58.89 &plusmn 5.49</th>
        <th><u>55.51 &plusmn 0.36</th>
    </tr>
    <tr>
        <th rowspan="3">SP</th>
        <th>MAE</th>
        <th>49.26 &plusmn 0.11</th>
        <th><u>48.39 &plusmn 0.19</th>
        <th>122.84 &plusmn 4.61</th>
        <th>55.70 &plusmn 0.01</th>
        <th>54.59 &plusmn 0.03</th>
        <th>49.12 &plusmn 0.17</th>
        <th>48.70 &plusmn 0.25</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>70.97 &plusmn 0.13</th>
        <th><u>69.48 &plusmn 0.62</th>
        <th>175.83 &plusmn 13.31</th>
        <th>79.94 &plusmn 0.01</th>
        <th>77.28 &plusmn 0.03</th>
        <th>70.95 &plusmn 0.34</th>
        <th>70.28 &plusmn 0.31</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>39.90 &plusmn 0.46</th>
        <th>38.25 &plusmn 1.95</th>
        <th>102.22 &plusmn 24.13</th>
        <th>47.80 &plusmn 0.10</th>
        <th>46.68 &plusmn 0.32</th>
        <th>38.51 &plusmn 0.41</th>
        <th><u>37.52 &plusmn 0.37</th>
    </tr>
    <tr>
        <th rowspan="3">SXB</th>
        <th>MAE</th>
        <th>80.33 &plusmn 0.24</th>
        <th><u>78.32 &plusmn 0.23</th>
        <th>262.40 &plusmn 0.00</th>
        <th>94.09 &plusmn 0.05</th>
        <th>89.88 &plusmn 0.17</th>
        <th>80.19 &plusmn 0.36</th>
        <th>78.71 &plusmn 0.29</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>142.42 &plusmn 0.73</th>
        <th><u>139.91 &plusmn 0.95</th>
        <th>363.49 &plusmn 0.00</th>
        <th>162.33 &plusmn 0.05</th>
        <th>156.75 &plusmn 0.32</th>
        <th>141.91 &plusmn 0.63</th>
        <th>141.32 &plusmn 0.36</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>40.29 &plusmn 0.54</th>
        <th>38.22 &plusmn 0.97</th>
        <th>223.27 &plusmn 0.00</th>
        <th>51.18 &plusmn 0.37</th>
        <th>49.09 &plusmn 0.17</th>
        <th>40.96 &plusmn 0.76</th>
        <th><u>37.89 &plusmn 0.11</th>
    </tr>
    <tr>
        <th rowspan="3">STR</th>
        <th>MAE</th>
        <th>61.10 &plusmn 0.38</th>
        <th>57.78 &plusmn 0.84</th>
        <th>71.86 &plusmn 5.01</th>
        <th>73.59 &plusmn 0.94</th>
        <th>68.30 &plusmn 0.33</th>
        <th><u>56.40 &plusmn 0.08</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>81.05 &plusmn 0.55</th>
        <th>74.94 &plusmn 1.18</th>
        <th>96.17 &plusmn 7.97</th>
        <th>96.18 &plusmn 1.48</th>
        <th>90.50 &plusmn 0.70</th>
        <th><u>73.46 &plusmn 0.06</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>22.32 &plusmn 0.19</th>
        <th>21.28 &plusmn 1.87</th>
        <th>25.56 &plusmn 2.23</th>
        <th>30.23 &plusmn 0.66</th>
        <th>25.02 &plusmn 1.17</th>
        <th><u>20.36 &plusmn 0.09</th>
        <th>OOM</th>
    </tr>
    <tr>
        <th rowspan="3">TPE</th>
        <th>MAE</th>
        <th>147.54 &plusmn 0.61</th>
        <th><u>140.98 &plusmn 2.89</th>
        <th>499.95 &plusmn 8.83</th>
        <th>163.96 &plusmn 0.02</th>
        <th>168.31 &plusmn 0.17</th>
        <th>142.71 &plusmn 0.55</th>
        <th>142.86 &plusmn 1.83</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>670.14 &plusmn 0.45</th>
        <th>671.29 &plusmn 2.58</th>
        <th>996.04 &plusmn 7.32</th>
        <th>726.80 &plusmn 0.40</th>
        <th>726.73 &plusmn 1.06</th>
        <th><u>666.42 &plusmn 0.36</th>
        <th>678.02 &plusmn 3.41</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>54.90 &plusmn 0.81</th>
        <th>47.50 &plusmn 4.82</th>
        <th>280.63 &plusmn 13.88</th>
        <th>52.22 &plusmn 0.17</th>
        <th>60.40 &plusmn 0.77</th>
        <th>45.94 &plusmn 2.11</th>
        <th><u>44.89 &plusmn 0.61</th>
    </tr>
    <tr>
        <th rowspan="3">TO</th>
        <th>MAE</th>
        <th>104.21 &plusmn 0.69</th>
        <th><u>92.97 &plusmn 2.72</th>
        <th>319.07 &plusmn 5.97</th>
        <th>106.30 &plusmn 0.02</th>
        <th>105.57 &plusmn 0.66</th>
        <th>139.93 &plusmn 0.61</th>
        <th>133.21 &plusmn 1.02</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>178.09 &plusmn 1.38</th>
        <th><u>154.59 &plusmn 2.71</th>
        <th>424.02 &plusmn 8.74</th>
        <th>182.49 &plusmn 0.32</th>
        <th>167.92 &plusmn 0.92</th>
        <th>231.65 &plusmn 2.32</th>
        <th>221.49 &plusmn 0.33</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>67.26 &plusmn 0.52</th>
        <th><u>51.82 &plusmn 1.26</th>
        <th>400.37 &plusmn 6.15</th>
        <th>59.46 &plusmn 1.38</th>
        <th>69.03 &plusmn 0.16</th>
        <th>82.81 &plusmn 0.41</th>
        <th>87.58 &plusmn 0.12</th>
    </tr>
    <tr>
        <th rowspan="3">YTO</th>
        <th>MAE</th>
        <th>57.16 &plusmn 0.24</th>
        <th><u>56.66 &plusmn 1.67</th>
        <th>173.86 &plusmn 9.18</th>
        <th>125.57 &plusmn 0.08</th>
        <th>74.96 &plusmn 1.04</th>
        <th>70.85 &plusmn 0.31</th>
        <th>60.80 &plusmn 0.21</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>94.09 &plusmn 0.11</th>
        <th><u>90.75 &plusmn 1.41</th>
        <th>253.42 &plusmn 9.38</th>
        <th>191.73 &plusmn 0.25</th>
        <th>114.34 &plusmn 1.97</th>
        <th>115.62 &plusmn 0.60</th>
        <th>100.24 &plusmn 0.45</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>44.91 &plusmn 1.53</th>
        <th><u>43.39 &plusmn 4.12</th>
        <th>128.97 &plusmn 45.99</th>
        <th>110.73 &plusmn 1.97</th>
        <th>73.18 &plusmn 1.56</th>
        <th>44.39 &plusmn 0.43</th>
        <th>43.66 &plusmn 0.17</th>
    </tr>
    <tr>
        <th rowspan="3">TLS</th>
        <th>MAE</th>
        <th>257.57 &plusmn 0.47</th>
        <th>255.17 &plusmn 0.18</th>
        <th>264.44 &plusmn 6.13</th>
        <th>264.06 &plusmn 0.00</th>
        <th>298.73 &plusmn 0.16</th>
        <th><u>255.11 &plusmn 0.01</th>
        <th>257.76 &plusmn 0.30</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>348.95 &plusmn 1.83</th>
        <th>342.20 &plusmn 1.02</th>
        <th>352.99 &plusmn 9.76</th>
        <th>348.31 &plusmn 0.02</th>
        <th>408.17 &plusmn 0.23</th>
        <th><u>340.28 &plusmn 0.14</th>
        <th>346.83 &plusmn 0.97</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>746.15 &plusmn 8.05</th>
        <th>758.84 &plusmn 36.31</th>
        <th>791.75 &plusmn 78.81</th>
        <th>867.12 &plusmn 0.77</th>
        <th>842.35 &plusmn 8.43</th>
        <th><u>745.07 &plusmn 5.77</th>
        <th>746.42 &plusmn 0.82</th>
    </tr>
    <tr>
        <th rowspan="3">UTC</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>55.13 &plusmn 4.47</th>
        <th>OOM</th>
        <th>57.76 &plusmn 0.72</th>
        <th>73.45 &plusmn 1.74</th>
        <th>73.81 &plusmn 0.57</th>
        <th><u>40.36 &plusmn 0.11</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>89.55 &plusmn 1.67</th>
        <th>OOM</th>
        <th>97.52 &plusmn 1.24</th>
        <th>109.98 &plusmn 1.82</th>
        <th>123.95 &plusmn 2.23</th>
        <th><u>75.86 &plusmn 0.31</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th>80.70 &plusmn 18.35</th>
        <th>OOM</th>
        <th>64.93 &plusmn 0.77</th>
        <th>105.19 &plusmn 2.55</th>
        <th>93.66 &plusmn 5.16</th>
        <th><u>40.85 &plusmn 2.82</th>
    </tr>
    <tr>
        <th rowspan="3">VNO</th>
        <th>MAE</th>
        <th>96.16 &plusmn 0.15</th>
        <th>91.31 &plusmn 0.19</th>
        <th>OOM</th>
        <th>81.71 &plusmn 4.58</th>
        <th>98.47 &plusmn 0.10</th>
        <th><u>80.01 &plusmn 0.59</th>
        <th>105.63 &plusmn 1.55</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>130.79 &plusmn 0.34</th>
        <th>124.11 &plusmn 0.44</th>
        <th>OOM</th>
        <th>111.45 &plusmn 2.76</th>
        <th>131.28 &plusmn 0.02</th>
        <th><u>109.93 &plusmn 0.18</th>
        <th>141.02 &plusmn 1.91</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>63.46 &plusmn 0.21</th>
        <th>58.74 &plusmn 1.31</th>
        <th>OOM</th>
        <th>47.91 &plusmn 8.96</th>
        <th>60.49 &plusmn 0.08</th>
        <th><u>46.17 &plusmn 1.50</th>
        <th>77.00 &plusmn 2.31</th>
    </tr>
    <tr>
        <th rowspan="3">WOB</th>
        <th>MAE</th>
        <th>56.73 &plusmn 0.26</th>
        <th><u>53.73 &plusmn 0.93</th>
        <th>65.57 &plusmn 0.76</th>
        <th>69.50 &plusmn 0.05</th>
        <th>61.35 &plusmn 0.11</th>
        <th>57.82 &plusmn 0.18</th>
        <th>56.30 &plusmn 0.43</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>90.97 &plusmn 0.48</th>
        <th><u>83.48 &plusmn 2.09</th>
        <th>104.61 &plusmn 1.31</th>
        <th>111.82 &plusmn 0.01</th>
        <th>92.81 &plusmn 0.13</th>
        <th>91.64 &plusmn 0.05</th>
        <th>89.31 &plusmn 0.69</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>42.48 &plusmn 1.04</th>
        <th><u>41.16 &plusmn 3.01</th>
        <th>53.82 &plusmn 1.86</th>
        <th>55.70 &plusmn 0.59</th>
        <th>54.53 &plusmn 0.12</th>
        <th>44.75 &plusmn 0.61</th>
        <th>43.14 &plusmn 1.57</th>
    </tr>
    <tr>
        <th rowspan="3">ZRH</th>
        <th>MAE</th>
        <th>OOM</th>
        <th>56.73 &plusmn 0.03</th>
        <th>OOM</th>
        <th>65.62 &plusmn 0.00</th>
        <th>65.29 &plusmn 0.20</th>
        <th>61.77 &plusmn 4.83</th>
        <th><u>54.71 &plusmn 0.20</th>
    </tr>
    <tr>
        <th>RMSE</th>
        <th>OOM</th>
        <th>80.80 &plusmn 0.23</th>
        <th>OOM</th>
        <th>94.06 &plusmn 0.01</th>
        <th>91.54 &plusmn 0.20</th>
        <th>88.03 &plusmn 6.88</th>
        <th><u>77.75 &plusmn 0.44</th>
    </tr>
    <tr>
        <th>MAPE(%)</th>
        <th>OOM</th>
        <th>36.22 &plusmn 0.43</th>
        <th>OOM</th>
        <th>47.73 &plusmn 0.13</th>
        <th>48.20 &plusmn 0.21</th>
        <th>46.66 &plusmn 8.57</th>
        <th><u>35.87 &plusmn 0.06</th>
    </tr>
</table>

