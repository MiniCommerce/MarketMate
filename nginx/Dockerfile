# 기본 이미지를 nginx로
FROM nginx

# 해당 경로의 해당 파일들 삭제
RUN rm /etc/nginx/nginx.conf && \
    rm /etc/nginx/conf.d/default.conf

# 해당 파일들을 해당 경로로 복사
COPY ./nginx.conf /etc/nginx/
COPY ./marketmate.conf /etc/nginx/conf.d/
