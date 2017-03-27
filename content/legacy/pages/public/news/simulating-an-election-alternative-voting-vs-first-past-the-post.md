# Simulating an election: Alternative Voting vs First-Past-the-Post
<br>

The news and social media are currently full of debate about the Alternative Voting system with the looming <a href="http://www.aboutmyvote.co.uk/5_may.aspx">referendum on the 5th May</a>.  Through your letterbox you've probably had a few leaflets describing the process and/or trying to persuade you to vote one way or another.  The NO camp seems focussed on how much it would cost to implement and that somehow a person who doesn't have the "most" votes can still win.  The YES camp, meanwhile, are trying to sell an "order of preference" argument and to convince you that AV means that all your votes count.

When I tried to decide which way to vote, I wondered how much validity there was in either side of the argument.  Would AV really drastically change the political landscape?  So like any good programmer I decided to carry out an experiment to see if I could get a better understanding of the AV process and what it might mean for us.  What follows is an account of an experiment which hopefully gives us some insight.

Note that this analysis includes some fundamental assumptions - they are skimmed over in the main text, and enumerated at the end for the interested reader.
<h2>Counting Alternative Votes</h2>

The NO to AV camp emphasises the complexity of the AV system, although actually the process is relatively straightforward (it just looks complex because it has a number of steps, but most of them are the same).  Here is a short description of the process, which you can skip if you already know how it works.

<ol>
    <li>Each voter ranks the candidates on the ballot in order of preference.  They may vote for as many candidates as they choose.</li>
    <li>In the first round of counting each ballot is counted based on the first preference on each ballot.  That is, each ballot is counted based only on the first ranked candidate.</li>
    <li>If a candidate has more than 50% of the total votes cast (not the total electorate in the constituency) then they win and there is no further counting.</li>
    <li>If not, the candidate with the fewest total votes is eliminated and their votes redistributed to the remaining candidates based on the second ranked candidate.  If the ballot does not have a second placed candidate it is discarded.</li>
    <li>If a candidate has more than 50% of the total votes cast then they win and there is no further counting</li>
    <li>If not, the next weakest candidate with the fewest total votes is eliminated and their votes redistributed to the remaining candidates.  This stage differs from stage 4 in that now the vote is given to the candidate who appears ranked highest on the ballot.  This is because the candidate in 2nd or 3rd place on the ballot may have already been eliminated from the counting.</li>
    <li>If a candidate has more than 50% of the total votes cast then they win and there is no further counting</li>
    <li>If not, go back to stage 6 and keep going until someone wins.  If no one ever gets more than 50% of the total vote, then by the time there are 2 candidates remaining the one with the most votes wins.</li>
</ol>
<h2>Similarities between AV and First Past The Post (FPTP)</h2>

AV effectively simplifies to FPTP in the event that all voters cast a single vote.  In this case the counting process would effectively cease at (3) above, as no subsequent re-distribution of votes would change the outcome.

AV also simplifies to FPTP in the event that there are only 2 candidates standing in a constituency; this is academic, as this never happens in normal events.

<h2>Simulating an Election</h2>

Ok, so how do you simulate a general election?  We've never had an AV election before so there's no data to indicate how it would work, the best we can do is approximate based on some realistic data.

The realistic data we used for this experiment was the 2010 General Election results, which you can get at the <a href="http://www.electoralcommission.org.uk/elections/results/general_elections">Electoral Commission's website</a>.  This data tells you, for each constituency, which parties stood and how many votes they got.

What we wanted to do was guess at how the election results might have looked if AV were in effect, and to do that we were going to have to generate imaginary votes based on this data.  We did this in the following way:

<strong>1. Assume that parties cluster</strong>

We assume that people who vote for a particular party are very unlikely to vote for certain parties, and very likely to consider voting for others.  For example, it is quite safe to assume that Labour voters are unlikely to vote Conservative as their second choice, and BNP voters unlikely to vote Green second.  The clustering that we used to obtain the results which are presented here is as follows (where the party codes are as defined in the Electoral Commission spreadsheet linked above).

<table>
<tbody>
<tr><th>1st Party (with abbreviation)</th><th>2nd, 3rd, 4th, etc parties</th></tr>
<tr>
<td>Alliance Party (APNI)</td>
<td>SF, DUP, SDLP, TUV, UCUNF</td>
</tr>
<tr>
<td>British National Party (BNP)</td>
<td>Ch P, Con, CPA, NF, UKIP</td>
</tr>
<tr>
<td>Christian Party (Ch P)</td>
<td>BNP, CPA, Con, ED</td>
</tr>
<tr>
<td>Conservative (Con)</td>
<td>LD, UKIP, ED, Ch P, CPA</td>
</tr>
<tr>
<td>Christian People's Alliance (CPA)</td>
<td>BNP, Ch P, Con, ED</td>
</tr>
<tr>
<td>Democratic Unionist Party (DUP)</td>
<td>SDLP, TUV, UCUNF, APNI</td>
</tr>
<tr>
<td>English Democrats (ED)</td>
<td>Con, BNP, NF, CPA, Ch P</td>
</tr>
<tr>
<td>Green Party (Grn)</td>
<td>LD, Lab, SDLP, PC, SSP, TUSC, TUV</td>
</tr>
<tr>
<td>Labour Party (Lab)</td>
<td>LD, Grn, SDLP, Soc, SSP, TUSC, TUV</td>
</tr>
<tr>
<td>Liberal Democrats (LD)</td>
<td>Lab, Con, Grn, PC, SDLP</td>
</tr>
<tr>
<td>Monster Raving Loony Party (MRLP)</td>
<td>Con, Lab, LD, Grn, PC, SDLP, SNP, SSP, UKIP</td>
</tr>
<tr>
<td>National Front (NF)</td>
<td>BNP, Con, ED, UKIP</td>
</tr>
<tr>
<td>Plaid Cymru (PC)</td>
<td>Con, Lab, LD</td>
</tr>
<tr>
<td>Respect (Respect)</td>
<td>Con, Lab, LD</td>
</tr>
<tr>
<td>Social Democratic & Labour Party (SDLP)</td>
<td>Grn, Lab, LD</td>
</tr>
<tr>
<td>Sinn Fein (SF)</td>
<td>APNI, USUNF</td>
</tr>
<tr>
<td>Socialist Labour Party (Soc)</td>
<td>Lab, SSP, SDLP, TUSC, TUV</td>
</tr>
<tr>
<td>Scottish National Party (SNP)</td>
<td>Ch P, CPA, UKIP</td>
</tr>
<tr>
<td>Scottish Socialist Party (SSP)</td>
<td>Grn, Lab, LD, SDLP, TUSC, TUV</td>
</tr>
<tr>
<td>Trade Unionist and Socialist Coalition (TUSC)</td>
<td>SDLP, Soc, SSP, TUV</td>
</tr>
<tr>
<td>Traditional Unionist Voice (TUV)</td>
<td>SDLP, Soc, SSP, TUSC</td>
</tr>
<tr>
<td>UUP and CON joint party (UCUNF)</td>
<td>APNI, SF, DUP</td>
</tr>
<tr>
<td>United Kingdon Independence Party (UKIP)</td>
<td>BNP, NF, Con</td>
</tr>
</tbody>
</table>

Note that we have only considered parties which fielded more than 10 candidates in the General Election; there were many smaller and independent candidates standing, bringing the total number of potential parties to around 130.

<strong>2. Assume that all votes are actual first choice</strong>

We construct the simulated AV ballots by assuming that the candidates people voted for in 2010 are the candidates that they would have put a "1" next to.

<strong>3. Assume that second, third, fourth, etc votes follow the same voting trends as first votes</strong>

This is where things get tricky.

First of all, for any individual ballot we decide how many votes are going to be cast on it.  We allow each ballot to have up to a maximum 4 votes (i.e. the numbers 1, 2, 3, 4 placed next to the candidates), and therefore select a number between 1 and 4 (with equal probability) for that particular ballot.  So 100% of people vote for at least 1 person, 75% for at least 2, 50% for at least 3, and 25% for 4.  No ballots contain more than 4 votes.

Let us use an example constituency to help us through this process.  This is the data from the 2010 election for Bedfordshire Mid:

<pre>Bedfordshire Mid; Electorate: 76310; Voter turnout: 54897
Con: 28815; ED: 712; Grn: 773; Lab: 8108; LD: 13663; UKIP: 2826</pre>

We place the first vote as per the 2010 general election;  So we allocate 28815 ballots with a Conservative "1" vote, 712 with an English Democrats "1" vote and so on.  Next, for each party standing in this constituency we look to see which other parties they cluster with, and cast the (potential) 2nd, 3rd and 4th votes based on that.

So, the Conservative party clustering is as follows (from the table above):

<pre>Conservative (Con) : LD, UKIP, ED, Ch P, CPA</pre>

That is, we assume that a Conservative voter would consider voting 2nd for the Liberal Democrats, UKIP, the English Democrats, the Christian Party or the Christian People's Alliance.  Given that in this case the Christian Party and the Christian People's Alliance are not fielding candidates, we consider only the Liberal Democrats, UKIP and the English Democrats.

The next step is to decide how likely a vote of "2" on this ballot is going to be for each of these parties.  We do that by looking at the number of votes each of these parties received <em>in the actual election</em>, and giving them a likelihood of being picked as a percentage of the total votes cast for these parties.  Thus:

<pre>Votes cast: ED: 712, LD: 13663, UKIP: 2826
Total votes cast for ED, LD and UKIP: 17201
Likelihood of being selected: ED: 4%, LD: 80%, UKIP: 16%</pre>

So we choose the 2nd vote at random but weight the likelihood by these percentages.  There is, then, an 80% chance that a Conservative voter who chooses to cast a 2nd vote (which is 75% of them) will vote Liberal Democrat.

Once this 2nd vote is cast (and let's assume that it was Liberal Democrat), then we cast the 3rd vote in the same way (for the 50% of voters that cast a 3rd vote), but eliminating the Liberal Democrats from the choices, thus:

<pre>Votes cast: ED: 712, UKIP: 2826
Total votes cast for ED and UKIP: 3538
Likelihood of being selected: ED: 20%, UKIP: 80%</pre>

So we choose the 3rd vote at random but with a 20% chance of choosing the English Democrats and an 80% chance of choosing UKIP.  And so on with this process until all allowed votes are used up or the list of candidates expires.

Now with these 3 stages complete we have generated ballots for every person who voted in the 2010 general election with guesses as to how they might have looked had we had an AV election rather than FPTP.  The final stage, then, is to simply count the results and see what changes.

<h2>Simulated Election Results</h2>

We have produced a full result set for a typical run of the simulation: <a href="https://bitbucket.org/richardjones/fptpvsav/raw/8adbb2e26515/GE2010-simulation.html">in HTML</a>, <a href="https://bitbucket.org/richardjones/fptpvsav/raw/8adbb2e26515/GE2010-simulation.csv">as a CSV</a>, <a href="https://bitbucket.org/richardjones/fptpvsav/raw/8adbb2e26515/GE2010-simulation.ods">as an OpenOffice.org spreadsheet</a>, <a href="https://bitbucket.org/richardjones/fptpvsav/raw/8adbb2e26515/GE2010-simulation.xls">as an Excel spreadsheet</a>.  Note that each run of the software (which can be download <a href="https://bitbucket.org/richardjones/fptpvsav/raw/8adbb2e26515/FPTPvsAV.py">here</a>) can generate slightly different results, through the random elements introduced, although the result set provided here is indicative. We have counted the results both using a FPTP and an AV algorithm, where the FPTP is simply the same as the 2010 election results.

There are two kinds of results which it is interesting to look at.

<strong>1. Safe seats</strong>

There are 222 seats where AV makes <em>no difference</em> to the FPTP result because the winning candidate already had more than 50% of the votes.  In these cases your 2nd, 3rd, 4th, etc votes are NOT counted.  This is not a product of the software and its assumptions, it is absolutely the case based on examination of the 2010 General Election results.

Examples of this are in Worcestershire West, St Helens North, and Liverpool Walton.

<strong>2. Alternative/Marginal Seats</strong>

There were only 49 seats where the AV system resulted in a change of the winning party.  The shift in ownership of the seats looks something like this:

<pre>Lab -> LD: 20 seats
Lab -> Con: 17 seats
Con -> LD: 11 seats
SNP -> Lab: 1 seat</pre>
This would give us the following difference to the actual outcome of the 2010 election:
<pre>Lab: -36 seats
LD: +31 seats
Con: +6 seats
SNP: -1 seats</pre>

Giving us an outcome in terms of seat count of:

<pre>Con: 312 seats
Lab: 222 seats
LD: 88 seats
SNP: 5 seats</pre>

<h2>Analysis</h2>

<strong>1. Marginal seats are more marginal</strong>

It's clear from randomly generated data that closely contested seats become more difficult to predict under AV.  Consider the following (artificial) setup:

<pre>Grn : 251, Con : 262, LD : 244, Lab : 243</pre>

This election is VERY close, but in FPTP it is Con with 262 votes who wins (despite only having 11 more votes than Grn).

But given the way that parties cluster, rounds of re-counting leave us with:

<pre>Grn: 487, LD: 513</pre>

So the Liberal Democrats take it in the end, despite being ranked 3rd in FPTP.

<strong>2. Allegiance is good</strong>

In seats with large numbers of parties, those which are closely aligned and in line with a mainstream party will ensure that the mainstream party is reinforced and elected.  It is therefore in the interests of the mainstream parties to foster relations with second- and third- tier parties

<strong>3. Small parties don't benefit</strong>

A corollary to (2) above is that AV doesn't appear to benefit small parties, it simply reinforces large parties which are allied with those smaller parties.  It does appear to lower the threshold at which a party becomes "large", though, as evidenced by the increase in seats received by the Liberal Democrats.

Notice that this simulation also predicted the SNP - a minor party - losing one of its 6 seats.

<strong>4. Vote proportion to seat proportion is only partially addressed</strong>

Given the actual votes that Labour, Conservative and Liberal Democrat received, the seat spread is still uneven:

<table border="1" cellpadding="3">
<tbody>
<tr>
<th>Party</th>
<th>Total votes nationwide</th>
<th>Vote proportion*</th>
<th>FPTP Seat Count</th>
<th>FPTP Seat proportion*</th>
<th>AV Seat Count</th>
<th>AV Seat proportion</th>
</tr>
<tr>
<td>Con</td>
<td>1181619</td>
<td>44%</td>
<td>306</td>
<td>49%</td>
<td>312</td>
<td>50%</td>
</tr>
<tr>
<td>Lab</td>
<td>836200</td>
<td>31%</td>
<td>258</td>
<td>42%</td>
<td>222</td>
<td>36%</td>
</tr>
<tr>
<td>LD</td>
<td>695668</td>
<td>25%</td>
<td>57</td>
<td>9%</td>
<td>88</td>
<td>14%</td>
</tr>
</tbody>
</table>
<em>* - calculated just between Con, Lab and LD - smaller parties have been omitted for simplicity</em>

This is, nonetheless, an important step for the Liberal Democrats.

<h2>Conclusions</h2>

It is clear from looking at the numbers why it is that the large parties are basically against AV and the Liberal Democrats are for it.

All the arguments provided by the YES and NO to AV camps also appear to be misleading.  Firstly, let's ignore the cost issue, it's nothing to do with whether it's a good idea to move to AV just whether we can afford to.  Effectively the two sides arguments are (with responses):

<strong>NO</strong>: the person who gets the most votes is the winner, the person who didn't get the most votes shouldn't be allowed to win

<strong>Response</strong>: the definition of "most" here is misleading, and this argument only applies to a two-horse race.  It is clear from examining votes with many candidates that the "best fit" candidate for "most" people is not strictly the one who got the "most" votes, but the one who represents the "most" interests.

<strong>YES</strong>: isn't it better to list your order of preference in case you can't have your first choice

<strong>Response</strong>: not all votes count (or are counted) in AV, despite what the arguments in its favour might say.  Even if you can't have your first choice that doesn't mean you can have your second choice either and indeed you can easily get something that wasn't on your list of preferences at all.

So which way should you vote?  Well, that's none of my business - I hope that the above has at least given you some insight into what we're voting for.  We've seen that both FPTP and AV are flawed in different ways.  The question is which set of flaws do you dislike the least.

<h2>Appendices</h2>

The bitbucket for the software is <a href="https://bitbucket.org/richardjones/fptpvsav">here</a>

<strong>Assumptions</strong>

The whole process described above rests on some assumptions which you may disagree with.  If you do, feel free to disregard this article altogether, or better still download the software and modify it to more accurately reflect what you think are the true assumptions.

<ol>
    <li>That people voted (in 2010) only for the party they actually wanted to win.  This model does not take into account strategic voting.</li>
    <li>The exact way that parties cluster is a matter of some debate, our treatment here is simplistic; a better solution would be to weight the relationships between different parties and infer the clusters that way</li>
    <li>People won't vote for more than 4 candidates, and that the probability distribution of how many candidates people vote for is flat</li>
    <li>That 2nd, 3rd, 4th, etc vote patterns will follow the same pattern as the FPTP election.  This is the most risky assumption, as it being wrong is both quite likely and destabilises the experiment somewhat.  Nonetheless, as the FPTP election results is the <em>only</em> realistic data we have to go on, it is still the best candidate for guessing how people would vote; possibly this could be alleviated by better treatment of party clustering</li>
      <li>That the very small parties and independent candidates have minimal effect on the outcome.  This assumption feels safe, but a full simulation with party clustering for all ~130 parties would be a valuable exercise, but beyond our capacity in the timeframe of the upcoming referendum</li>
</ol>



Original Title: Simulating an Election: Alternative Voting vs First-Past-the-Post
Original Author: richard
Tags: alternative voting, politics, richard, python, news
Created: 2011-04-28 1115
Last Modified: 2013-08-28 1056
