<details>
 <summary>
  Data Integrity Suite
 </summary>
 <table id="T_8f9c8">
  <thead>
   <tr>
    <th class="col_heading level0 col0" id="T_8f9c8_level0_col0">
     Status
    </th>
    <th class="col_heading level0 col1" id="T_8f9c8_level0_col1">
     Check
    </th>
    <th class="col_heading level0 col2" id="T_8f9c8_level0_col2">
     Condition
    </th>
    <th class="col_heading level0 col3" id="T_8f9c8_level0_col3">
     More Info
    </th>
   </tr>
  </thead>
  <tbody>
   <tr>
    <td class="data row0 col0" id="T_8f9c8_row0_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row0 col1" id="T_8f9c8_row0_col1">
     Single Value in Column
    </td>
    <td class="data row0 col2" id="T_8f9c8_row0_col2">
     Does not contain only a single value
    </td>
    <td class="data row0 col3" id="T_8f9c8_row0_col3">
     Passed for 10 relevant columns
    </td>
   </tr>
   <tr>
    <td class="data row1 col0" id="T_8f9c8_row1_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row1 col1" id="T_8f9c8_row1_col1">
     Special Characters
    </td>
    <td class="data row1 col2" id="T_8f9c8_row1_col2">
     Ratio of samples containing solely special character is less or equal to 0.1%
    </td>
    <td class="data row1 col3" id="T_8f9c8_row1_col3">
     Passed for 10 relevant columns
    </td>
   </tr>
   <tr>
    <td class="data row2 col0" id="T_8f9c8_row2_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row2 col1" id="T_8f9c8_row2_col1">
     Mixed Nulls
    </td>
    <td class="data row2 col2" id="T_8f9c8_row2_col2">
     Number of different null types is less or equal to 1
    </td>
    <td class="data row2 col3" id="T_8f9c8_row2_col3">
     Passed for 10 relevant columns
    </td>
   </tr>
   <tr>
    <td class="data row3 col0" id="T_8f9c8_row3_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row3 col1" id="T_8f9c8_row3_col1">
     String Mismatch
    </td>
    <td class="data row3 col2" id="T_8f9c8_row3_col2">
     No string variants
    </td>
    <td class="data row3 col3" id="T_8f9c8_row3_col3">
     Passed for 1 relevant column
    </td>
   </tr>
   <tr>
    <td class="data row4 col0" id="T_8f9c8_row4_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row4 col1" id="T_8f9c8_row4_col1">
     Data Duplicates
    </td>
    <td class="data row4 col2" id="T_8f9c8_row4_col2">
     Duplicate data ratio is less or equal to 5%
    </td>
    <td class="data row4 col3" id="T_8f9c8_row4_col3">
     Found 0% duplicate data
    </td>
   </tr>
   <tr>
    <td class="data row5 col0" id="T_8f9c8_row5_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row5 col1" id="T_8f9c8_row5_col1">
     String Length Out Of Bounds
    </td>
    <td class="data row5 col2" id="T_8f9c8_row5_col2">
     Ratio of string length outliers is less or equal to 0%
    </td>
    <td class="data row5 col3" id="T_8f9c8_row5_col3">
     Passed for 1 relevant column
    </td>
   </tr>
   <tr>
    <td class="data row6 col0" id="T_8f9c8_row6_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row6 col1" id="T_8f9c8_row6_col1">
     Conflicting Labels
    </td>
    <td class="data row6 col2" id="T_8f9c8_row6_col2">
     Ambiguous sample ratio is less or equal to 0%
    </td>
    <td class="data row6 col3" id="T_8f9c8_row6_col3">
     Ratio of samples with conflicting labels: 0%
    </td>
   </tr>
   <tr>
    <td class="data row7 col0" id="T_8f9c8_row7_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row7 col1" id="T_8f9c8_row7_col1">
     Feature Label Correlation
    </td>
    <td class="data row7 col2" id="T_8f9c8_row7_col2">
     Features' Predictive Power Score is less than 0.8
    </td>
    <td class="data row7 col3" id="T_8f9c8_row7_col3">
     Passed for 9 relevant columns
    </td>
   </tr>
   <tr>
    <td class="data row8 col0" id="T_8f9c8_row8_col0">
     <div style="color: green;text-align: center">
      ✓
     </div>
    </td>
    <td class="data row8 col1" id="T_8f9c8_row8_col1">
     Feature-Feature Correlation
    </td>
    <td class="data row8 col2" id="T_8f9c8_row8_col2">
     Not more than 0 pairs are correlated above 0.9
    </td>
    <td class="data row8 col3" id="T_8f9c8_row8_col3">
     All correlations are less than 0.9 except pairs []
    </td>
   </tr>
  </tbody>
 </table>
</details>
