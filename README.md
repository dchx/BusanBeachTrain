[English](README.md) | [中文](README_zh.md)

One of Busan's most famous attractions is the capsule train. The capsule train operates at Haeundae Blue Line Park (<https://www.bluelinepark.com>). Besides the capsule train (Sky Capsule), Blue Line Park also features a vintage train called the Beach Train. The Beach Train has seven stations:

A. 미포 Mipo  
This station connects to the downtown area of Haeundae District and is located at the eastern end of Haeundae Beach. Mipo Station also serves as a stop for the capsule train.

B. 달맞이터널 Dalmaji Tunnel  
A short tunnel featuring a mountain-side walkway.

C. 해월전망대 Haewol Skywalk  
A white skywalk extending over the sea, culminating in a circular glass walkway.

D. 청사포 Cheongsapo  
Cheongsapo Station is a hub where you can transfer to the capsule train. Adjacent to the station is a level crossing where rail and road meet. Due to the Beach Train passing through, it resembles the popular photo spot in Kamakura, Japan, making it a trendy destination for photos.

E. 다릿돌전망대 Daritdol Skywalk  
A blue skywalk extending into the sea.

F. 구덕포 Gudeokpo  
A coastal town located at the western end of Songjeong Beach.

G. 송정 Songjeong  
Another developed area built along Songjeong Beach.

Coastal Train tickets include single-ride, double-ride, and pass options, allowing one boarding at any single station, two stations, or all seven stations respectively. After boarding, passengers may ride in either direction and disembark at any station, but must exit at the terminal stations (Mipo or Songjeong).

We purchased a pass ticket, starting from Mipo toward Songjeong, disembarking at every station for a stroll. After reaching Songjeong, we returned directly to Mipo—effectively completing one round trip. However, by adjusting travel strategies, more round trips could be possible. I summarized it as the following problem:

> There is a railway with seven stations: A, B, C, D, E, F, G. The terminal stations are A and G. There are trains in both directions that stop at every station. A pass ticket allows boarding at each of the seven stations exactly once. At all stations excluding the terminals, passengers may ride in either direction. They may disembark at any station, but all passengers must exit when the train reaches terminal stations A or G. We define the segment of railway between any two adjacent stations as a section. If I purchase this pass ticket, how should I travel to maximize the number of sections I traverse? Repeated sections count toward the total. In this travel plan, I may walk from one station to another after disembarking, but each walk is limited to a maximum of x sections. If multiple plans yield the maximum number of traversed sections, select the one with the minimum number of total walking sections. Choose the optimal travel plan and compute the maximum number of traversed sections for x = 0, 1, 2, 3.

If I'm not afraid of walking, I can get off at a station and walk to any other one to board again. Then, after boarding at each station, I can travel the maximum distance possible from that station—meaning I can board and ride to the farthest terminal station from that point. Thus, boarding from stations A-G, I could travel 6, 5, 4, 3, 4, 5, and 6 sections respectively, totaling 33 sections—equivalent to 2.75 round trips. This represents the maximum number of sections possible with a pass ticket, but the maximum walking distance is 3 sections (i.e., x = 3), the case when I'd return from one terminal station to D Cheongsapo Station. A sample travel plan for this scenario is: ride A->G, ride G->A, walk A->B, ride B->G, walk G->F, ride F->A, walk A->C, ride C->G, walk G->E, ride E->A, walk A->D, ride D->G.

However, if I start from D Cheongsapo Station, I no longer need to return to Cheongsapo to ride. In this case, the maximum walking distance is 2 segments (i.e., x = 2), the case when walking from one terminal station to C Haewol Skywalk or E Daritdol Skywalk. This also achieves the goal of traveling from each station to the terminal station farthest from it. The maximum number of sections remains 33. A sample travel plan for this scenario is: ride D->A, ride A->G, ride G->A, walk A->B, ride B->G, walk G->F, ride F->A, walk A->C, ride C->G, walk G->E, ride E->A.

On the other hand, if I do not accept walking, I must board at the same station where I disembark (i.e., x = 0). A tentative solution is: ride A->G->B->F->C->E->D->G, totaling 24 sections. This travel plan roughly traces a damped oscillation pattern. Observing this plan reveals that, due to the "no walking" constraint, each station typically involves one boarding and one disembarking, except for the starting and ending stations of the travel. For the ending station, one can freely choose without being restricted by the "no walking" condition, so A Mipo Station or G Songjeong Station are usually selected. For the starting station, a key feature is that it is not subject to the "must disembark at this station once" restriction. Where is the least advantageous station to disembark? It's the middle station D Cheongsapo. Given this, we might designate Cheongsapo as the starting station, thereby avoiding disembarking there. Under this scenario, one sample plan is: ride D->G->A->F->B->E->C->G, traversing 27 sections. Subsequent trials revealed that once the starting station is fixed, altering intermediate boarding/disembarking stations appears to have no impact on the maximum number of sections traversed.

Is this 27-section (2.25 round trips) plan the optimal solution? When I posed this question to AIs, many failed to achieve 27 sections under the x = 0 condition. Numerous responses yielded 24 sections, while others misinterpreted the problem. I then asked AI to write a code to solve this problem. It (Gemini 2.5 Pro) generated a code using a recursive function for brute-force search, stating its time complexity as O(2ⁿn³) and space complexity as O(2ⁿn²).

`beachtrain.py` is the code, and `solution.txt` contains the results of running the code.
