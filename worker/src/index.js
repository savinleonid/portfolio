const projects = [
  {
    id: "kayra-ai",
    name: "Kayra AI",
    platforms: ["web"],
    stack: ["React", "Vue.js", "FastAPI", "REST API"],
  },
  {
    id: "handme",
    name: "HandMe",
    platforms: ["android", "ios"],
    stack: ["Flutter", "Dart", "REST API"],
  },
];

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json; charset=utf-8",
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: corsHeaders });
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    if (request.method === "GET" && url.pathname === "/health") {
      return json({ status: "ok", timestamp: new Date().toISOString() });
    }

    if (request.method === "GET" && url.pathname === "/v1/projects") {
      const platform = url.searchParams.get("platform");
      const result = platform
        ? projects.filter((project) => project.platforms.includes(platform))
        : projects;
      return json(result);
    }

    if (request.method === "POST" && url.pathname === "/v1/contact-requests") {
      let body;
      try {
        body = await request.json();
      } catch {
        return json({ detail: "Тело запроса должно быть JSON." }, 422);
      }

      const validEmail = typeof body.email === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email);
      if (
        typeof body.name !== "string" || !body.name.trim() ||
        !validEmail ||
        typeof body.message !== "string" || !body.message.trim()
      ) {
        return json({ detail: "Укажите имя, корректный email и описание задачи." }, 422);
      }

      return json(
        {
          id: crypto.randomUUID(),
          status: "accepted",
          createdAt: new Date().toISOString(),
          note: "Демонстрационный endpoint: заявка не сохраняется.",
        },
        201,
      );
    }

    return json({ detail: "Маршрут не найден." }, 404);
  },
};
