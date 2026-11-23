# Day one, day seven — NEON DODGE

A short vertical video about the same tiny agent-built game on the day it
was made and after a week of daily updates.

The game is **NEON DODGE**, a tiny dodger: steer the ship, dodge the falling
blocks, grab the coins. Day 1 is the same map and the same start with 3 slow
grey blocks and nothing else. Day 7 is the same map and the same start, but
after seven days of daily updates it is visibly busier: 14 fast coloured
blocks, gold coins, particle trails, a combo counter and a score that climbs
fast. The camera never moves, so the change is the whole story.

The video (1080x1920, H.264 + AAC, 24 s) was made in this session:
`gen_frames.py` renders the gameplay frames for both versions of the game,
`filter.txt` is the ffmpeg filter graph that cuts them together with the
on-screen text, the make.fun brand badge and the press-pack referral end
card (with referral code `hgbjgrd6` typed into its field), and the result is
`day-one-day-seven-tiktok.mp4`.

## The video

The video is posted publicly on TikTok by pemar from @pemalangairdrop as a
video (not a photo post), viewers set to Everyone, with no edit, trim or
effect in TikTok's editor. Caption:

> Day one vs day seven of my tiny game NEON DODGE — same map, same start, seven days of updates later it's a different game. Made by my AI agent for a $20 bounty on make.fun: make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327 makefun-sugar-tundra-lute

## Entry

`main.ts` copies `VIDEO.json` from the repository to the output directory.
`VIDEO.json` holds the video's full TikTok address once it is posted.
