### how2compile

Doing part of rust compilation and check some condition in the intermidate product.

So you'll get a "double reverse" experience, first realize the binary is doing comiling-and-comparing, then extract and recover the compared IR into source.

The recovered source is another flag checker, but I think there is already enough recursive and omit the flag here.

### Issues

The first version of the challenge will print the IR, so there will be unintended trivial flag leak using `include_bytes!` or sth like that. :(

The attachments here is the fixed version.
