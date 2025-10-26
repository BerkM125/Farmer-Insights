Inspiration
Our team was inspired by AI's disruptive ability to create our own AI-powered disruptive technology to improve the agricultural sector. Realizing how much harder it is for small farmers to compete with industrial agricultural firms, we decided to create Demeter, an app providing enterprise-grade agricultural insights to small farmers in an incredibly affordable, convenient platform. We were driven not just by Demeter's potential to bring equitable solutions to small farmers, but also by the innovative technical stack (involving satellite data, agentic AI, web scraping, and more) we would need to learn in order to build this platform.

From studying past digital solutions made for small farmers in more remote areas (such as DigitalGreen's FarmerChat, with conclusive data from over 15K users), we determined that small farmers appreciated straightforward answers when they looked to solve an issue on the farm. However, text-only chatbots have a limited problem-solving scope, cannot communicate complex live data, and struggle to address real-time issues that are tied to a farmer's environmental, climatic, economic, and ecological conditions. We drew from the conclusions of past studies AI farming assistants to develop a more powerful solution that bakes complex, data-driven analysis of farms right into an intuitive mobile interface.

What it does
Demeter is a mobile chat app and analytics dashboard that small farmers can consult about any and all problems they encounter on their farms. Farmers can ask Demeter how to address problems like a bad harvest, a crop infection, droughts, or seasonal changes, and Demeter will respond with recommended action items and strategies to help them overcome their issues. Farmers can also take pictures of their crops or plants and send them to the chatbot to diagnose issues like pests, disease, drought, or other puzzling conditions.

All of Demeter's strategies are informed by a combination of satellite data, regional environmental data, and agricultural market data (e.g, commodity prices, the price of the farmer's crop, etc) which can be found on the other pages of the Demeter app. Demeter features:

Updated satellite footage and analysis tools, where farmers can observe high-res images of water, moisture, vegetation, and crop health distribution across their entire farm.
Topsoil and environmental health analysis tools, where farmers can observe soil pH levels across their farms along with other environmental data (e.g, soil nitrogen levels).
Market data and analysis tools, where farmers get real-time prices and market data to allow them to make the best decisions about harvesting, selling, and pricing their produce.
Every page of Demeter features action items that farmers can follow to address issues that Demeter is passively picking up on. For example, Demeter will prescribe steps to address drought if it detects oncoming dryness over satellite footage, or it will recommend liming (pH/acid neutralizing) if it detects excessively acidic pH levels.

How we built it
Demeter is a mobile web application built with SvelteKit. At the core of our app, we have a LLM chatbot (run through Lava Gateway) that has access to a Supabase database containing a variety of different realtime data, including satellite data, weather data, market price data, and soil data. This data is collected by a group of Fetch.ai agents, which collaborate to keep the database up to date. The central LLM also has access to a Chroma vector database of farming and agricultural data, such as crop manuals, from which it can semantically search for knowledge. We also used CodeRabbit to review and help merge PRs.

Challenges we ran into
We ran into:

Network issues
Difficulties with harnessing up-to-date satellite data
Difficulties with ensuring that the model learns continuously (context engineering)
Accomplishments that we're proud of
We're very proud to have successfully implemented all the steps of our data flow and tech stack that we planned from the start. We're proud to have been able to learn technologies that were very new to us, like Google Earth Engine and Fetch.ai, and create a working application with a complex architecture.

What we learned
We learned how to use a team of agents to effectively solve real-world problems and prescribe practical strategies. We learned how to use highly diverse datasets, from vector embeddings to structured satellite data, to craft truly effective strategies within the app.

What's next for Demeter
A public launch! We believe Demeter has great potential in the real world to solve problems for many small farmers. Beyond that, we feel that there is great potential for more data sources and further personalization to each farmer.