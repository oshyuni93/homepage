document.addEventListener('DOMContentLoaded', () => {
  // gnb > ul > li > a 마우스 오버 또는 focus 시 .header-inner 높이를 .gnb 높이로 변경
  const gnb = document.querySelector('#gnb');
  const header = document.querySelector('.header');
  const gnbLinks = gnb.querySelectorAll('ul > li > a');
  
  gnbLinks.forEach(link => {
    if( window.innerWidth < 1024) {
      link.closest('ul').addEventListener('mouseover', () => {
        header.style.height = `6.5rem`;
      });
    } else {
      link.closest('ul').addEventListener('mouseover', () => {
        header.style.height = `${gnb.offsetHeight}px`;
      });
      link.addEventListener('focus', () => {
        header.style.height = `${gnb.offsetHeight}px`;
      });
    }
    
    link.closest('ul').addEventListener('mouseout', () => {
      if (window.innerWidth <= 1300) {
        header.style.height = '8rem';
      } else if(window.innerWidth <= 1024) {
        header.style.height = '6.5rem';
      } else {
        header.style.height = '10rem';
      }
    });
    link.addEventListener('blur', () => {
      if (window.innerWidth <= 1300) {
        header.style.height = '8rem';
      } else if(window.innerWidth <= 1024) {
        header.style.height = '6.5rem';
      } else {
        header.style.height = '10rem';
      }
    });
  });		

  //스크롤을 내릴때 .visual이나 .sub-visual의 영역을 넘어가면 .header에 .bg 클래스를 추가
  const visual = document.querySelector('.visual');
  const subVisuals = document.querySelector('.sub-visual');
  const headers = document.querySelector('.header');
  const headerHeight = header.offsetHeight;
  let isHeaderBgAdded = false;
  const logoImg = document.querySelector('.header-inner img');
  window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (visual && scrollTop > visual.offsetHeight - headerHeight && !isHeaderBgAdded) {
      headers.classList.add('bg');
      isHeaderBgAdded = true;      
      if (logoImg) {
        logoImg.src = '/assets/images/common/logo2.svg';
        logoImg.alt = 'BGROUND 로고';
      }
    } else if (subVisuals && scrollTop > subVisuals.offsetHeight - headerHeight && !isHeaderBgAdded) {
      headers.classList.add('bg');
      isHeaderBgAdded = true;
      if (logoImg) {
        logoImg.src = '/assets/images/common/logo2.svg';
        logoImg.alt = 'BGROUND 로고';
      }
    } else if (scrollTop <= (visual ? visual.offsetHeight : 0) - headerHeight || scrollTop <= (subVisual ? subVisual.offsetHeight : 0) - headerHeight) {
      headers.classList.remove('bg');
      isHeaderBgAdded = false;
      if (logoImg) {
        logoImg.src = '/assets/images/common/logo.svg';
        logoImg.alt = 'BGROUND 로고';
      }
    }
  });

  //width 1024px 이상에서 스크롤을  내리면 header를 숨기고 위로 올리면 header를 보이게 함
  let lastScrollTop = 0;
  window.addEventListener('scroll', () => {
      const header = document.querySelector('.header');
      const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
      console.log('currentScrollTop:', currentScrollTop, 'lastScrollTop:', lastScrollTop);
      if (currentScrollTop > lastScrollTop) {
        // 스크롤을 내릴 때
        header.style.top = '-100px'; // 헤더 숨기기
      } else {
        // 스크롤을 올릴 때
        header.style.top = '0'; // 헤더 보이기
      }
      lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop; // For Mobile or negative scrolling
  })
  
  

  //mobile gnb
  // 모바일 gnb submenu 토글 이벤트는 한 번만 바인딩
  let mobileSubMenuBound = false;
  function bindMobileSubMenu() {
    if (mobileSubMenuBound) return;
    document.querySelectorAll('.gnb > ul > li.sub > a').forEach(function (item) {
      item.addEventListener('click', function (e) {
        if (window.innerWidth > 1024) return;
        e.preventDefault();
        document.querySelector('.header').style.height = 'auto';
        const subMenu = this.nextElementSibling;
        if (subMenu.style.display === 'block') {
          subMenu.style.display = 'none';
        } else {
          subMenu.style.display = 'block';
        }
      });
    });
    mobileSubMenuBound = true;
  }
  bindMobileSubMenu();
  window.addEventListener('resize', function() {
    // 필요시 추가 동작
  });

  //.btn-m-menu 버튼 클릭 시 모바일 메뉴 토글
  const btnMobileMenu = document.querySelector('.btn-m-menu');
  if (btnMobileMenu) {
    btnMobileMenu.addEventListener('click', function () {      
      const mobileGnb = document.querySelector('.header-inner .gnb');        
      if (mobileGnb) {
        mobileGnb.classList.add('on');
      }
      const dim = document.querySelector('.dim'); 
      if (dim) {
        dim.classList.add('on');
      }
      document.body.style.overflow = 'hidden';
    });
  }
  // 모바일 메뉴 닫기
  const btnCloseMobileMenu = document.querySelector('.btn-menu-close');
  if (btnCloseMobileMenu) {
    btnCloseMobileMenu.addEventListener('click', function () {
      const mobileGnb = document.querySelector('.header-inner .gnb');
      mobileGnb.classList.remove('on');
      const dim = document.querySelector('.dim'); 
      if (dim) {
        dim.classList.remove('on');
      }
      document.body.style.overflow = '';
    });
  }
  //gnb 외부 클릭 시 모바일 메뉴 닫기
  document.addEventListener('click', function (e) {
    const mobileGnb = document.querySelector('.header-inner .gnb');
    if (mobileGnb && !mobileGnb.contains(e.target) && !btnMobileMenu.contains(e.target)) {
      mobileGnb.classList.remove('on');
      const dim = document.querySelector('.dim'); 
      if (dim) {
        dim.classList.remove('on');
      }
      document.body.style.overflow = '';
    }
  });
  
  // sub-visual 로딩시 클래스 on 추가
  const subVisual = document.querySelector('.sub-visual');
  if (subVisual) {
    window.addEventListener('load', () => {
      subVisual.classList.add('on');
    });
  }
})