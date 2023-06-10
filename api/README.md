# `karpathy-gpt-api`

This it is the back-end for Karpathy-GPT.

### `Test locally` - 

Set API keys: 
```
export OPENAI_API_KEY=xxx
```

Start local server:
```
uvicorn karpathy_app:app
```

Inputs:
```
question
```

Test doc retrieval:
```
curl -X POST -F "question=What is makemore" http://localhost:8000/karpathy-docs
```

```
data: page_content="Hi everyone, hope you're well. And next up what I'd like to do is I'd like to build out Makemore. Like Micrograd before it, Makemore is a repository that I have on my GitHub web page. You can look at it. But just like with Micrograd, I'm going to build it out step by step and I'm going to spell everything out. So we're going to build it out slowly and together. Now, what is Makemore? Makemore, as the name suggests, makes more of things that you give it. So here's an example. Names.txt is an example dataset to Makemore. And when you look at Names.txt, you'll find that it's a very large dataset of names. So here's lots of different types of names. In fact, I believe there are 32,000 names that I've sort of found randomly on a government website. And if you train Makemore on this dataset, it will learn to make more of things like this. And in particular, in this case, that will mean more things that sound name-like, but are actually unique names. And maybe if you have a baby and you're trying to assign a name, maybe you're looking for a cool new sounding unique name, Makemore might help you. So here are some example generations from the neural network once we train it on our dataset. So here's some example unique names that it will generate. Don't tell, I rot, Zendi, and so on. And so all these sort of sound name-like, but they're not, of course, names. So under the hood, Makemore is a character-level language model. So what that means is that it is treating every single line" metadata={'id': '02', 'link': 'https://youtu.be/PaCmpygFfXo', 'source': 'The spelled-out intro to language modeling： building makemore 02', 'title': 'The spelled-out intro to language modeling： building makemore'}

data: page_content="not, of course, names. So under the hood, Makemore is a character-level language model. So what that means is that it is treating every single line here as an example. And within each example, it's treating them all as sequences of individual characters. So R-E-E-S-E is this example, and that's the sequence of characters. And that's the level on which we are building out Makemore. And what it means to be a character-level language model, then, is that it's just sort of modeling those sequences of characters, and it knows how to predict the next character in the sequence. Now, we're actually going to implement a large number of character-level language models in terms of the neural networks that are involved in predicting the next character in a sequence. So very simple bigram and bag-of-word models, multilayered perceptrons, recurrent neural networks, all the way to modern transformers. In fact, the transformer that we will build will be basically the equivalent transformer to GPT-2, if you have heard of GPT. So that's kind of a big deal. It's a modern network, and by the end of the series, you will actually understand how that works on the level of characters. Now, to give you a sense of the extensions here, after characters, we will probably spend some time on the word level, so that we can generate documents of words, not just little segments of characters, but we can generate entire large, much larger documents. And then we're probably going to go into images and" metadata={'id': '02', 'link': 'https://youtu.be/PaCmpygFfXo', 'source': 'The spelled-out intro to language modeling： building makemore 02', 'title': 'The spelled-out intro to language modeling： building makemore'}

data: page_content="Hi everyone. Today we are continuing our implementation of MakeMore, our favorite character-level language model. Now, you'll notice that the background behind me is different. That's because I am in Kyoto and it is awesome. So I'm in a hotel room here. Now, over the last few lectures, we've built up to this architecture that is a multi-layer perceptron character-level language model. So we see that it receives three previous characters and tries to predict the fourth character in a sequence using a very simple multi-layer perceptron using one hidden layer of neurons with tenational neurons. So what I'd like to do now in this lecture is I'd like to complexify this architecture. In particular, we would like to take more characters in a sequence as an input, not just three. And in addition to that, we don't just want to feed them all into a single hidden layer because that squashes too much information too quickly. Instead, we would like to make a deeper model that progressively fuses this information to make its guess about the next character in a sequence. And so we'll see that as we make this architecture more complex, we're actually going to arrive at something that looks very much like a WaveNet. So WaveNet is this paper published by Dequined in 2016. And it is also a language model, basically, but it tries to predict audio sequences instead of character-level sequences or word-level sequences. But fundamentally, the modeling setup is identical. It is an autoregressive" metadata={'id': '06', 'link': 'htt
```

Test answer stream:

```
curl -X POST -F "question=What is makemore" http://localhost:8000/karpathy-stream
```

```
data: M

data: ak

data: em

data: ore

data:  is

data:  a

data:  character

data: -level

data:  language

data:  model
```

### `Test deployed API -`  

We deploy as an API to [Railway](https://railway.app/).
 
Test:
```
curl -X POST -F "question=What is makemore" https://karpathy-gpt-production.up.railway.app/karpathy-stream
```

Returns streaming events, as shown above.