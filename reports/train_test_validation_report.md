<details>
 <summary>
  Train Test Validation Suite
 </summary>
 <table id="T_1ac23">
  <thead>
   <tr>
    <th class="col_heading level0 col0" id="T_1ac23_level0_col0">
     Status
    </th>
    <th class="col_heading level0 col1" id="T_1ac23_level0_col1">
     Check
    </th>
    <th class="col_heading level0 col2" id="T_1ac23_level0_col2">
     Condition
    </th>
    <th class="col_heading level0 col3" id="T_1ac23_level0_col3">
     More Info
    </th>
   </tr>
  </thead>
  <tbody>
   <tr>
    <td class="data row0 col0" id="T_1ac23_row0_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row0 col1" id="T_1ac23_row0_col1">
     Datasets Size Comparison
    </td>
    <td class="data row0 col2" id="T_1ac23_row0_col2">
     Test-Train size ratio is greater than 0.01
    </td>
    <td class="data row0 col3" id="T_1ac23_row0_col3">
     Test-Train size ratio is 0.43
    </td>
   </tr>
   <tr>
    <td class="data row1 col0" id="T_1ac23_row1_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row1 col1" id="T_1ac23_row1_col1">
     New Label Train Test
    </td>
    <td class="data row1 col2" id="T_1ac23_row1_col2">
     Number of new label values is less or equal to 0
    </td>
    <td class="data row1 col3" id="T_1ac23_row1_col3">
     Found 0 new labels in test data: []
    </td>
   </tr>
   <tr>
    <td class="data row2 col0" id="T_1ac23_row2_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row2 col1" id="T_1ac23_row2_col1">
     New Category Train Test
    </td>
    <td class="data row2 col2" id="T_1ac23_row2_col2">
     Ratio of samples with a new category is less or equal to 0%
    </td>
    <td class="data row2 col3" id="T_1ac23_row2_col3">
     Passed for 4 relevant features
    </td>
   </tr>
   <tr>
    <td class="data row3 col0" id="T_1ac23_row3_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row3 col1" id="T_1ac23_row3_col1">
     String Mismatch Comparison
    </td>
    <td class="data row3 col2" id="T_1ac23_row3_col2">
     No new variants allowed in test data
    </td>
    <td class="data row3 col3" id="T_1ac23_row3_col3">
     Passed for 3 relevant columns
    </td>
   </tr>
   <tr>
    <td class="data row4 col0" id="T_1ac23_row4_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row4 col1" id="T_1ac23_row4_col1">
     Train Test Samples Mix
    </td>
    <td class="data row4 col2" id="T_1ac23_row4_col2">
     Percentage of test data samples that appear in train data is less or equal to 5%
    </td>
    <td class="data row4 col3" id="T_1ac23_row4_col3">
     No samples mix found
    </td>
   </tr>
   <tr>
    <td class="data row5 col0" id="T_1ac23_row5_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row5 col1" id="T_1ac23_row5_col1">
     Feature Label Correlation Change
    </td>
    <td class="data row5 col2" id="T_1ac23_row5_col2">
     Train-Test features' Predictive Power Score difference is less than 0.2
    </td>
    <td class="data row5 col3" id="T_1ac23_row5_col3">
     Passed for 9 relevant columns
    </td>
   </tr>
   <tr>
    <td class="data row6 col0" id="T_1ac23_row6_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row6 col1" id="T_1ac23_row6_col1">
     Feature Label Correlation Change
    </td>
    <td class="data row6 col2" id="T_1ac23_row6_col2">
     Train features' Predictive Power Score is less than 0.7
    </td>
    <td class="data row6 col3" id="T_1ac23_row6_col3">
     Passed for 9 relevant columns
    </td>
   </tr>
   <tr>
    <td class="data row7 col0" id="T_1ac23_row7_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row7 col1" id="T_1ac23_row7_col1">
     Feature Drift
    </td>
    <td class="data row7 col2" id="T_1ac23_row7_col2">
     categorical drift score &lt; 0.2 and numerical drift score &lt; 0.2
    </td>
    <td class="data row7 col3" id="T_1ac23_row7_col3">
     Passed for 8 columns out of 8 columns.
Found column "cat1" has the highest categorical drift score: 0
Found column "cont4" has the highest numerical drift score: 7.13E-3
    </td>
   </tr>
   <tr>
    <td class="data row8 col0" id="T_1ac23_row8_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row8 col1" id="T_1ac23_row8_col1">
     Label Drift
    </td>
    <td class="data row8 col2" id="T_1ac23_row8_col2">
     Label drift score &lt; 0.15
    </td>
    <td class="data row8 col3" id="T_1ac23_row8_col3">
     Label's drift score Cramer's V is 0
    </td>
   </tr>
   <tr>
    <td class="data row9 col0" id="T_1ac23_row9_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row9 col1" id="T_1ac23_row9_col1">
     Multivariate Drift
    </td>
    <td class="data row9 col2" id="T_1ac23_row9_col2">
     Drift value is less than 0.25
    </td>
    <td class="data row9 col3" id="T_1ac23_row9_col3">
     Found drift value of: 0, corresponding to a domain classifier AUC of: 0.49
    </td>
   </tr>
  </tbody>
 </table>
</details>
