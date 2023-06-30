# Recommendation

So, how can our result now be used for recommendation?

Remember that in our business case Netflix uses an alogorithmus that gives every kid a recommendation which movie to watch. At this point it still recommends every kid with the same algorithm like for adults.

This now can be changed. Now we want that this algortim uses our popularity table.

So how will the algorithm use it?

Every time a kid opens Netflix, this algorithm will connect to our database and check which movies are the most popular. Then it will use this information to recomment specific movies. Maybe this algorithm will also consider other information, like the user behaviour of the children. But this is not information that we provided. We only provide the information which movies are popular for kids in general.

This is a use case where we use data NOT to create a dashboard that a humand reads. We created data that will be automatically consumed by other programs.