// functions/api/list.js - 修复版

export async function onRequest(context) {
  try {
    const { request } = context;
    const url = new URL(request.url);

    const page = parseInt(url.searchParams.get('page')) || 1;
    const pageSize = parseInt(url.searchParams.get('size')) || 30;

    if (page < 1 || pageSize < 1 || pageSize > 100) {
      return new Response(JSON.stringify({
        error: '参数错误'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // ★★★ 方法一：使用相对路径 ★★★
    const jsonUrl = '/data/wallpapers.json';
    
    // ★★★ 方法二：使用绝对路径（备选） ★★★
    // const jsonUrl = `${url.protocol}//${url.host}/data/wallpapers.json`;

    const resp = await fetch(jsonUrl, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'CloudflarePages-Function'
      }
    });

    if (!resp.ok) {
      return new Response(JSON.stringify({
        error: `无法加载壁纸数据 (HTTP ${resp.status})`
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const allData = await resp.json();

    if (!Array.isArray(allData) || allData.length === 0) {
      return new Response(JSON.stringify({
        code: 0,
        data: {
          items: [],
          total: 0,
          page: 1,
          pageSize: pageSize,
          totalPages: 0,
          hasMore: false
        }
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=3600',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // 按日期降序排列
    const sortedData = [...allData].sort((a, b) => b.date.localeCompare(a.date));

    const total = sortedData.length;
    const totalPages = Math.ceil(total / pageSize);
    const start = (page - 1) * pageSize;
    const end = Math.min(start + pageSize, total);
    const items = sortedData.slice(start, end);

    return new Response(JSON.stringify({
      code: 0,
      data: {
        items: items,
        total: total,
        page: page,
        pageSize: pageSize,
        totalPages: totalPages,
        hasMore: page < totalPages
      }
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*'
      }
    });

  } catch (error) {
    return new Response(JSON.stringify({
      error: '服务器错误',
      message: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
