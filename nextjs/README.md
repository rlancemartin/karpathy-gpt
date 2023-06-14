## Testing

To run front-end locally with you locally running back-end, simply change the source in `fetchEventSource` [here](https://github.com/rlancemartin/karpathy-gpt/blob/a338ceb8666c02b0ec7e7f47ca0a196d774d1e4d/nextjs/pages/index.tsx#L37) and [here](https://github.com/rlancemartin/karpathy-gpt/blob/a338ceb8666c02b0ec7e7f47ca0a196d774d1e4d/nextjs/pages/index.tsx#L55) to `http://localhost:8000/karpathy-docs` and `http://localhost:8000/karpathy-stream`
* To run the front-end locally, run:
```
npm run dev
```

## Credits

Thanks to [Mckay Wrigley](https://twitter.com/mckaywrigley) for open-sourcing his UI.

Thanks to Karapthy for the excellent course.ß

## Contact

If you have any questions, feel free to reach out to me on [Twitter](https://twitter.com/RLanceMartin)!
