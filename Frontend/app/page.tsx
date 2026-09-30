import { redirect } from "next/navigation"

export default function Page() {
  // The deliverable is a single self-contained HTML file served from /index.html
  redirect("/index.html")
}
