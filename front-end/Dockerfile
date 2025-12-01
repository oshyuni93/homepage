# nginx 공식 이미지를 기반으로 사용
FROM nginx:alpine

# 작업 디렉토리 설정
WORKDIR /usr/share/nginx/html

# 기존 nginx 기본 페이지 삭제
RUN rm -rf ./*

# 현재 프로젝트의 모든 파일을 nginx html 디렉토리로 복사
COPY . /usr/share/nginx/html

# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 80 포트 노출
EXPOSE 80

# nginx 실행 (기본 명령어 사용)
CMD ["nginx", "-g", "daemon off;"] 