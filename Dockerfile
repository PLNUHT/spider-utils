FROM node:lts-alpine
WORKDIR /build
RUN npm install user-agents
RUN echo "const ua = require('user-agents');for(let i = 0; i < 10000; ++ i) console.log( (new ua({'deviceCategory': 'desktop'})).toString() );" | node - > ualist.txt

FROM python:3.7
WORKDIR /build
RUN pip install psycopg2 pyquery -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
COPY --from=0 /build/ualist.txt spider_utils/ualist.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python setup.py install
