# tearx
Browse the web from your terminal like a real hacker.

tearx scrapes data from searxng sites, as long as they don't modify the site too much. The application also has very modern features such as caching, multi-language queries, cool ansi sequences and more. See `tearx -h`.

Please don't judge the source code. I'll do a rewrite soon™.

## "Installation"
```
echo "alias tearx=\"python3 $(pwd)/tearx\"" >> ~/.bashrc && source ~/.bashrc
```
Make sure tearx can access `~/.tearx/`.