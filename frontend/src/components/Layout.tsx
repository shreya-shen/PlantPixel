
import React from 'react';
import { Leaf, BarChart3, History, Camera } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();

  const navigation = [
    { name: 'Analyze', href: '/', icon: Camera },
    { name: 'Results', href: '/results', icon: BarChart3 },
    { name: 'History', href: '/history', icon: History },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-plant-50 via-sky-50 to-earth-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-plant-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-plant-gradient rounded-xl flex items-center justify-center">
                <Leaf className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-plant-gradient bg-clip-text text-transparent">
                  Plant Pixel
                </h1>
                <p className="text-xs text-gray-600">Plant Growth Analysis Platform</p>
              </div>
            </div>

            <nav className="flex space-x-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 ${
                      isActive
                        ? 'bg-plant-gradient text-white shadow-lg'
                        : 'text-gray-600 hover:bg-plant-100 hover:text-plant-700'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="hidden sm:block font-medium">{item.name}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;
