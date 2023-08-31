# 기본 이미지를 nginx로
FROM nginx

RUN rm /etc/nginx/nginx.conf && \
    rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/
COPY ./marketmate.conf /etc/nginx/conf.d/
