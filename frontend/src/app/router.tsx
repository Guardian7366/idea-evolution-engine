import { createBrowserRouter } from 'react-router-dom'

import { MainLayout } from '../layouts/MainLayout'
import { IdeaWorkspacePage } from '../pages/IdeaWorkspacePage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <MainLayout>
        <IdeaWorkspacePage />
      </MainLayout>
    ),
  },
])