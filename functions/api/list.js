// functions/api/list.js - 修改后的完整版本

export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);

  const page = parseInt(url.searchParams.get('page')) || 1;
  const pageSize = parseInt(url.searchParams.get('size')) || 30;
  const region = url.searchParams.get('region') || 'zh-CN'; // ★★★ 新增地区参数 ★★★

  if (page < 1) {
    return new Response(JSON.stringify({
      error: 'page 参数必须大于等于 1'
    }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  if (pageSize < 1 || pageSize > 100) {
    return new Response(JSON.stringify({
      error: 'size 参数必须在 1-100 之间'
    }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const host = url.origin;
    
    // ★★★ 优先使用完整版数据（含地区），如果没有则回退到默认 ★★★
    let fullJsonUrl = `${host}/data/wallpapers_full.json`;
    let fetchResp = await fetch(fullJsonUrl, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'CloudflarePages-Function'
      }
    });

    let useFullData = fetchResp.ok;
    let allData;

    if (useFullData) {
      allData = await fetchResp.json();
    } else {
      // 回退到兼容版
      const jsonUrl = `${host}/data/wallpapers.json`;
      fetchResp = await fetch(jsonUrl, {
        headers: {
          'Accept': 'application/json',
          'User-Agent': 'CloudflarePages-Function'
        }
      });
      if (!fetchResp.ok) {
        return new Response(JSON.stringify({
          error: '无法加载壁纸数据'
        }), {
          status: 502,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      const fallbackData = await fetchResp.json();
      // 将兼容版数据包装成完整版格式
      allData = fallbackData.map(item => ({
        date: item.date,
        regions: { 'zh-CN': item },
        copyright: item.copyright,
        description: item.description,
        jpg: item.jpg,
        webp: item.webp,
        thumb: item.thumb
      }));
    }

    if (!Array.isArray(allData) || allData.length === 0) {
      return new Response(JSON.stringify({
        error: '暂无壁纸数据'
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // ★★★ 根据地区筛选数据 ★★★
    let filteredData = allData.map(item => {
      // 如果数据有 regions 字段，提取指定地区的数据
      if (item.regions && item.regions[region]) {
        const r = item.regions[region];
        return {
          date: item.date,
          copyright: r.title,
          description: r.description,
          jpg: r.jpg,
          webp: r.webp,
          thumb: r.thumb,
          region: region
        };
      }
      // 如果指定地区不存在，回退到第一个可用地区
      else if (item.regions && Object.keys(item.regions).length > 0) {
        const firstRegion = Object.keys(item.regions)[0];
        const r = item.regions[firstRegion];
        return {
          date: item.date,
          copyright: r.title,
          description: r.description,
          jpg: r.jpg,
          webp: r.webp,
          thumb: r.thumb,
          region: firstRegion
        };
      }
      // 兼容旧格式
      else {
        return {
          date: item.date,
          copyright: item.copyright || '',
          description: item.description || '',
          jpg: item.jpg || '',
          webp: item.webp || '',
          thumb: item.thumb || '',
          region: 'zh-CN'
        };
      }
    }).filter(item => item !== null);

    // ★★★ 分页 ★★★
    const sortedData = filteredData.sort((a, b) => b.date.localeCompare(a.date));
    const total = sortedData.length;
    const totalPages = Math.ceil(total / pageSize);
    const start = (page - 1) * pageSize;
    const end = Math.min(start + pageSize, total);
    const items = sortedData.slice(start, end);

    return new Response(JSON.stringify({
      code: 0,
      data: {
        items: items,
        page: page,
        pageSize: pageSize,
        total: total,
        totalPages: totalPages,
        hasMore: page < totalPages,
        currentRegion: region
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
