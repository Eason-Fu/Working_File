# 我的工作文件

该库主要记录了我在日常学习、科研工作进行过程中学习编写的项目代码。


**目录：**

**2024.11  |  可以用于预清理超大数据表的项目**  |  ./PatentData_Processing/241111_InitialProcessingRawData & CutYears  |   原文件为从马克数据网上下载的4.5G的“上市公司-专利明细数据完整版（1988-2023年）”，内含有约270万条数据，直接使用excel无法打开并且会溢出，且含有大量不需要的杂音变量。本项目利用Pandas的分块读取功能读取原始文件，并清洗出需要的变量。案例保存了2005年以来数据，并选择了个别变量，使得文件小了一半。文件CutYears采用分块读取保存的方式，使05-10年,06-11年,07-12年...的数据循环保存为若干个小文件，方便读取或后续处理；InitialProcessingRawData则清洗了不需要的变量，保留需要的变量和年份。

**2024.11  |  一款可以自动清理并生成企业层面控制变量的项目**  |  ./Cleaning Data/241113_ConstructControlVariable  |   从CSMAR网站下载数据表后，不同表格的格式存在较大差异，且限于经济原因，你并不总能拥有所有表格的下载权。而在网络上购买的控制变量并不能及时更新，且其可信度、完整度以及计算方法都令人生疑；如果你希望稍微调整计算方法（以使结果更显著），在网络上购买的现成品也并不能支持你的期待，并且你还不一定能够准确简单地加工出你期望的新颖控制变量。为安全且省心的生成符合科研要求的控制变量表，本项目基于几个CSMAR提供的相对基础的公司研究表，给出了企业层面常见控制变量的生成方式。

**2024.11  |  匹配相同专利申请号并赋值上市代码的项目**  |  ./PatentData_Processing/241122_MatchFirmID(Basedon_Application)  |   在Incopat根据检索条目下载的专利数据范围过广，囊括了上市公司/外国企业/科研机构/学校/其他企业，并且缺少上市代码项，而根据研究需要希望筛选出Incopat数据内仅包括上市企业的专利，并为其赋予上市企业代码。Incopat数据和马克数据网的数据有共同项“专利申请号”，可以以此为关键字进行匹配，将马克数据网专利信息的企业上市代码变量赋值给Incopat数据，并将Incopat中有值的企业专利提取为一个文件。这个项目可以作为基准文件，衍生适用于“文件A/B含有相同关键字，提取B的某项变量赋值给A”类需求。

**2024.11  |  匹配企业社会统一信用代码并赋值上市代码的项目**  |  ./PatentData_Processing/241126_MatchFirmID(Basedon_USCC)  |   继承1122的项目，我们进一步考虑，基于上市企业社会统一信用代码作为关键字，将从CSMAR下载的企业上市代码赋值给Incopat专利文件（这样是从企业层面赋值，效果可能更优于专利层面赋值，因为马克数据网数据未必准确），参见241126_MatchFirmID(Basedon_USCC)。后补充：此后偶然从一篇文献中发现已有相同的做法，参考曲如晓等（2024）的《专利出海与中国企业对外直接投资》，其原文如“....由于该数据库所记录的企业上市代码不全,并且存在同一专利有两个或多个上市企业申请人的情况,本文将企业所对应的工商统一社会信用代码与上市企业证券代码进行匹配,再经手工对照和整理得到中国上市企业在海外各国的专利申请记录。”

# My working files

This library mainly records the project codes I learned and written during my daily study and scientific research work.


**Table of contents:**

**2024.11 | Projects that can be used to pre-clean very large data tables**  |  ./PatentData_Processing/241111_InitialProcessingRawData & CutYears  |  The original file is a 4.5G "Listed Company - Patent Detailed Data Complete Version (1988-2023)" downloaded from the Mark Data Network. It contains about 2.7 million pieces of data. It cannot be opened directly using Excel and will overflow. It also contains a large number of inaccuracies. Required noise variables. This project uses the block reading function of Pandas to read the original file and clean out the required variables. The case saves data since 2005 and selects individual variables, making the file half the size.

**2024.11  |  A project that can automatically clean and generate enterprise-level control variables**  |  ./Cleaning Data/241113_ConstructControlVariable  |  After downloading the data table from the CSMAR website, the formats of different tables are quite different, and are limited to economic reasons. You don't always have download rights for all forms. The control variables purchased on the Internet cannot be updated in time, and their credibility, completeness and calculation methods are questionable; if you want to slightly adjust the calculation method (to make the results more significant), the control variables purchased on the Internet Ready-made products cannot support your expectations, and you may not be able to accurately and simply process the novel control variables you expect. In order to safely and worry-freely generate control variable tables that meet scientific research requirements, this project is based on several relatively basic company research tables provided by CSMAR, and provides ways to generate common control variables at the enterprise level.

**2024.11 | Project to match the same patent application number and assign listing code** | ./PatentData_Processing/241122_MatchFirmID(Basedon_Application) | The scope of patent data downloaded from Incopat based on the search terms is too broad, covering listed companies/foreign companies/research institutions/schools/other companies, and lacks listing code items. According to research needs, we hope to filter out patents that only include listed companies in the Incopat data and assign them listing company codes. Incopat data and Mark Data Network data have a common item "patent application number", which can be used as a keyword for matching, assigning the company listing code variable of Mark Data Network patent information to Incopat data, and extracting the company patents with values ​​in Incopat into a file. This project can be used as a benchmark file, and is derived to be applicable to the requirements of "files A/B contain the same keywords, extract a variable of B and assign it to A". 

**2024.11 | Project to match corporate social unified credit code and assign listing code** | ./PatentData_Processing/241126_MatchFirmID(Basedon_USCC) | Inheriting the project of 1122, we further considered assigning the corporate listing code downloaded from CSMAR to the Incopat patent file based on the social unified credit code of the listed company as a keyword (this is to assign values ​​at the corporate level, which may be better than assigning values ​​at the patent level, because the data on the Mark Data Network may not be accurate), see 241126_MatchFirmID(Basedon_USCC). Later supplement: Later, I accidentally found a similar practice in a literature. Refer to Qu Ruxiao et al. (2024) "Patents Going Abroad and China's Outward Direct Investment", the original text of which is as follows: "....Since the corporate listing codes recorded in the database are incomplete, and there are two or more listed company applicants for the same patent, this paper matches the corresponding corporate unified social credit code with the listed company's securities code, and then obtains the patent application records of Chinese listed companies in overseas countries through manual comparison and sorting."
