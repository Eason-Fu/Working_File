# 我的工作文件

该库主要记录了我在日常学习、科研工作进行过程中学习编写的项目代码。


**目录：**

**2024.11  |  可以用于预清理超大数据表的项目**  |  ./PatentData_Processing/241111_InitialProcessingRawData & CutYears  |   原文件为从马克数据网上下载的4.5G的“上市公司-专利明细数据完整版（1988-2023年）”，内含有约270万条数据，直接使用excel无法打开并且会溢出，且含有大量不需要的杂音变量。本项目利用Pandas的分块读取功能读取原始文件，并清洗出需要的变量。案例保存了2005年以来数据，并选择了个别变量，使得文件小了一半。

**2024.11  |  一款可以自动清理并生成企业层面控制变量的项目**  |  ./Cleaning Data/241113_ConstructControlVariable  |   从CSMAR网站下载数据表后，不同表格的格式存在较大差异，且限于经济原因，你并不总能拥有所有表格的下载权。而在网络上购买的控制变量并不能及时更新，且其可信度、完整度以及计算方法都令人生疑；如果你希望稍微调整计算方法（以使结果更显著），在网络上购买的现成品也并不能支持你的期待，并且你还不一定能够准确简单地加工出你期望的新颖控制变量。为安全且省心的生成符合科研要求的控制变量表，本项目基于几个CSMAR提供的相对基础的公司研究表，给出了企业层面常见控制变量的生成方式。


# My working files

This library mainly records the project codes I learned and written during my daily study and scientific research work.


**Table of contents:**

**2024.11 | Projects that can be used to pre-clean very large data tables**  |  ./PatentData_Processing/241111_InitialProcessingRawData & CutYears  |  The original file is a 4.5G "Listed Company - Patent Detailed Data Complete Version (1988-2023)" downloaded from the Mark Data Network. It contains about 2.7 million pieces of data. It cannot be opened directly using Excel and will overflow. It also contains a large number of inaccuracies. Required noise variables. This project uses the block reading function of Pandas to read the original file and clean out the required variables. The case saves data since 2005 and selects individual variables, making the file half the size.

**2024.11  |  A project that can automatically clean and generate enterprise-level control variables**  |  ./Cleaning Data/241113_ConstructControlVariable  |  After downloading the data table from the CSMAR website, the formats of different tables are quite different, and are limited to economic reasons. You don't always have download rights for all forms. The control variables purchased on the Internet cannot be updated in time, and their credibility, completeness and calculation methods are questionable; if you want to slightly adjust the calculation method (to make the results more significant), the control variables purchased on the Internet Ready-made products cannot support your expectations, and you may not be able to accurately and simply process the novel control variables you expect. In order to safely and worry-freely generate control variable tables that meet scientific research requirements, this project is based on several relatively basic company research tables provided by CSMAR, and provides ways to generate common control variables at the enterprise level.
