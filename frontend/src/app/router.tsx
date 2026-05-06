import { createBrowserRouter } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import IdeaWorkspacePage from "../pages/IdeaWorkspacePage";

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <MainLayout>
        <IdeaWorkspacePage />
      </MainLayout>
    ),
  },
]);

export default router;