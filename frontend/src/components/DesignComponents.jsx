import React from 'react';
import { Button } from './ui';
import Card, { CardBody } from './ui';

/**
 * Lightweight, consistent design components
 * - Uses shared ui Button and Card for consistent spacing and accessible controls
 * - Cleaner defaults for production-ready layout
 */

export function Hero({
  title = 'Design inspired by Dribbble',
  subtitle = 'A demo gallery layout for integrating design elements into your healthcare agent application.',
  cta = 'Get started'
}) {
  return (
    <section className="bg-gradient-to-r from-indigo-600 to-pink-600 rounded-xl p-6 md:p-10 text-white shadow-md">
      <div className="md:flex md:items-center md:justify-between gap-6">
        <div className="max-w-2xl">
          <h2 className="text-2xl md:text-4xl font-extrabold leading-tight">{title}</h2>
          <p className="mt-3 text-sm md:text-lg text-white/90">{subtitle}</p>
        </div>

        <div className="mt-4 md:mt-0">
          <Button variant="secondary" size="md" aria-label="Get started">
            {cta}
          </Button>
        </div>
      </div>
    </section>
  );
}

function GalleryCard({ img, title, desc, assets }) {
  return (
    <Card className="overflow-hidden">
      <CardBody className="p-0">
        <img className="w-full h-40 object-cover rounded-t-lg" src={img} alt={title} />
        <div className="p-4">
          <h4 className="font-semibold text-lg text-white">{title}</h4>
          <p className="mt-2 text-sm text-gray-300">{desc}</p>
          <div className="mt-4 flex items-center justify-between">
            <div className="text-sm text-gray-400">{assets} assets</div>
            <Button variant="ghost" size="sm">View</Button>
          </div>
        </div>
      </CardBody>
    </Card>
  );
}

export default function Gallery({ items = [] }) {
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl md:text-2xl font-semibold text-white">Gallery</h3>
        <div className="text-sm text-gray-400">Updated designs and assets</div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((it, i) => (
          <GalleryCard
            key={i}
            img={it.img || `https://source.unsplash.com/collection/190727/800x600?sig=${i}`}
            title={it.title || `Design Card ${i + 1}`}
            desc={it.desc || 'Mockup image and short description'}
            assets={it.assets || 5}
          />
        ))}
      </div>
    </div>
  );
}