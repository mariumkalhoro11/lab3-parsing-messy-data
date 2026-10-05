# lab3-parsing-messy-data

## Comparison of Regex and AI-Assisted Cleaning

For this lab, I compared a regex-based Python cleaning approach with an AI-assisted cleaning approach using the same `messy_samples.csv` file. Overall, the two approaches agreed on most of the records after the values were standardized. Both methods were able to clean the sample IDs, dates of birth, sex values, enrollment sites, glucose units, and notes into a more consistent format.

One area where both methods did well was standardizing categorical values. For example, the sex column had values such as `M`, `m`, `Male`, `F`, `f`, `Female`, `U`, `unknown`, and blank values. Both approaches converted these into the consistent categories `Male`, `Female`, and `Unknown`. The enrollment site column also had several different versions of the same site, including `SITE-A`, `site_a`, `siteB`, `Site  C`, and values with extra spaces. These were standardized into `Site A`, `Site B`, and `Site C`.

The date field was more challenging because the dataset used several different formats. Some dates were already written in ISO format, such as `1957-02-27`, while others used slashes, periods, or month names, such as `07/09/1962`, `11.24.53`, and `05-Dec-1968`. My regex script had to include rules for each of these formats. The AI-assisted approach handled these different formats more quickly because I did not have to write a separate parsing rule for every variation.

The regex approach took more effort at the beginning because I had to write, test, and adjust the rules in Python. However, after the script was working, it was easier to understand exactly what was happening to each value. The rules were also reproducible, meaning I could run the same script again and get the same output.

The AI-assisted approach was faster for creating the first cleaned version of the dataset. It was able to recognize that values like `site_a` and `SITE-A` represented the same category without needing an exact regex rule for each version. However, I would be more careful about relying completely on AI for a real health dataset because the AI can make interpretations that are not directly shown in the raw data.

For a real clinical dataset, I would trust the regex/programmatic method more for the final cleaning pipeline because the transformations are explicit, testable, and reproducible. I think AI would still be useful as a secondary tool for finding unusual values, identifying possible edge cases, and helping develop cleaning rules faster.

## Specific Agreements and Edge Cases

One clear example of agreement was record `S0012`. The original sex value was blank and the enrollment site was written as `site_a`. Both approaches standardized the sex value to `Unknown` and the site to `Site A`.

Another example was `s-0003`. The original sample ID used a lowercase letter and a hyphen. The cleaned version standardized it to `S0003`. This shows how relatively simple formatting inconsistencies can be handled well by both methods.

Record `S0039` was more unusual because the original glucose value was written as `241.2*`. Both approaches were able to extract the numeric value `241.2`, but the asterisk is important because it may indicate that the original value was flagged. This shows that simply extracting the number can remove information from the raw record if the cleaning process does not preserve the meaning of special symbols.

## Failure Mode 1: Ambiguous Two-Digit Years

Record `S0017` had the date of birth `07.16.15`. My cleaning process interpreted this as `2015-07-16`.

The problem is that a two-digit year does not contain enough information by itself to prove the correct century. The value `15` could theoretically mean 1915 or 2015. Based on the other dates in the dataset, 2015 seems more reasonable, but this is still an assumption.

This is a failure mode because both regex and AI can make a reasonable-looking result even when the original data is ambiguous. In a real health dataset, I would want additional metadata or validation rules before assuming the century.

## Failure Mode 2: Suspicious mmol/L Glucose Values

A second failure mode appeared in records where glucose was labeled as `mmol/L`. For example, record `S0006` contained a glucose value of `159.9 mmol/L`.

Using the mathematical conversion from mmol/L to mg/dL produces a value of about `2881.1 mg/dL`, which is extremely high. Other examples in the dataset produced similarly large converted values.

The regex script followed the conversion rule exactly, so technically the calculation worked. The problem is that the original unit may be incorrect or intentionally messy. A program cannot automatically know whether the number is wrong, the unit is wrong, or the value is actually intended to be interpreted another way.

The AI-assisted approach has the same limitation. It can recognize the unit and perform the conversion, but it should not silently decide that the original unit was incorrect without evidence. This was one of the most important edge cases in the dataset because it shows the difference between formatting a value correctly and knowing whether the underlying data is actually valid.

## Time and Effort Comparison

The AI-assisted approach was faster at the beginning because I could provide the raw records and instructions and receive a structured version without manually writing a rule for every format. This was especially helpful for recognizing inconsistent capitalization, spacing, and category names.

The regex approach took more time because I had to create functions for sample IDs, dates, sex values, sites, glucose values, and units. I also had to test the script and fix errors before it produced the final output file.

Even though regex took longer, I felt more confident in the final process because I could see exactly how every value was being changed. For this reason, I would use AI to help explore messy data and find patterns, but I would use tested programmatic rules for the final version of a real health-data cleaning workflow.