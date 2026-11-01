#include "EBlindDLC.h"
#include "WatermarkReference.h"

#include <random>
#include <fstream>
#include <iostream>
#include <charconv>


EBlindDLC::EBlindDLC(double alpha, double detectThreshold, const std::vector<double> reference, Detector::Type detectorType): Watermark(),
	m_alpha(alpha),
	m_detectThreshold(detectThreshold),
	m_reference(reference),
	m_detectorType(detectorType)
{
}

EBlindDLC::~EBlindDLC()
{
}

void EBlindDLC::setAlpha(double alpha)
{
	m_alpha = alpha;
}

void EBlindDLC::setDetectThreshold(double detectThreshold)
{
	m_detectThreshold = detectThreshold;
}

void EBlindDLC::setReference(std::vector<double>& reference)
{
	m_reference = reference;
}


bool EBlindDLC::embed(std::shared_ptr<VideoFrame> pframe, bool value)
{
	if (m_alpha < 0)
		return false;

	if (!pframe)
		return false;

	std::size_t frameSize = pframe->width() * pframe->height();
	if (pframe->colorFormat() == VideoFrame::Color)
		frameSize *= 3;

	if (frameSize != m_reference.size())
		return false;

	int stride = pframe->stride(0);
	int widthColor = pframe->width() * (pframe->colorFormat() == VideoFrame::Color ? 3 : 1);
	uint8_t* pdata = pframe->data(0);

	for (int i = 0; i < pframe->height(); i++)
	{
		for (int j = 0; j < widthColor; j++)
		{
			int val = pdata[i * stride + j];
			int res = val + m_reference[i * widthColor + j] * m_alpha;
			if (res < 0)
				res = 0;
			if (res > 255)
				res = 255;

			pdata[i * stride + j] = res;
		}
	}

	return true;
}

EBlindDLC::DetectResult EBlindDLC::detect(const std::shared_ptr<VideoFrame> pframe)
{
	return detectInternal(pframe, NULL);
}

bool EBlindDLC::getCorrelation(const std::shared_ptr<VideoFrame> pframe, double& correlation)
{
	correlation = -1;
	detectInternal(pframe, &correlation);
	return true;
}

EBlindDLC::DetectResult EBlindDLC::detectInternal(const std::shared_ptr<VideoFrame> pframe, double* pcorrelation)
{
	if (m_detectThreshold < 0)
		return EBlindDLC::FAILED;

	if (!pframe)
		return EBlindDLC::FAILED;

	std::size_t frameSize = pframe->width() * pframe->height();
	int pixelSize = 1;
	if (pframe->colorFormat() == VideoFrame::Color)
	{
		frameSize *= 3;
		pixelSize = 3;
	}

	if (frameSize != m_reference.size())
		return EBlindDLC::FAILED;

	Detector::Result res = Detector::Result::FAILED;

	std::vector<double> data, noise;
	data.reserve(frameSize);

	uint8_t* pdata = pframe->data(0);


	for (std::size_t i = 0; i < pframe->height(); i++)
	{
		data.insert(data.end(), pdata + i * pframe->stride(0), pdata + i * pframe->stride(0) + pframe->width() * pixelSize);
	}

	if (m_detectorType == Detector::CORRELATION_COEFFICIENT)
	{
		res = Detector::CorrelationCoefficient(data, m_reference, m_detectThreshold, pcorrelation);
	}
	else if (m_detectorType == Detector::LINEAR)
	{
		res = Detector::LinearCorrelation(data, m_reference, m_detectThreshold, pcorrelation);
	}
	else if (m_detectorType == Detector::NORMALIZED)
	{
		res = Detector::NormalizedCorrelation(data, m_reference, m_detectThreshold, pcorrelation);
	}
	else if (m_detectorType == Detector::PEARSON_COEFFICIENT)
	{
		res = Detector::PearsonCorrelation(data, m_reference, m_detectThreshold, pcorrelation);
	}

	return (EBlindDLC::DetectResult) res;
}

std::vector<double> EBlindDLC::createReference(const std::shared_ptr<VideoFrame> pframe)
{
	std::size_t referenceSize = pframe->width() * pframe->height();
	if (pframe->colorFormat() == VideoFrame::Color)
		referenceSize *= 3;

	std::vector<double> reference(referenceSize);

	std::random_device rd;
	std::mt19937 gen(rd());
	std::normal_distribution<double> dist(0.0, 1.0);  // mean=0, stddev=1

	for (std::size_t i = 0; i < reference.size(); i++)
	{
		double val = dist(gen);
		reference[i] = val;
	}

	return reference;
}

void EBlindDLC::referenceStore(const std::vector<double>& data, const std::string& filename)
{
	std::ofstream file(filename, std::ios::binary);

	file.write(reinterpret_cast<const char*>(data.data()), data.size() * sizeof(double));
}

std::vector<double> EBlindDLC::referenceLoad(const std::string& filename)
{
	std::ifstream file(filename, std::ios::binary | std::ios::ate);
	if (!file) throw std::runtime_error("Cannot open file " + filename);

	std::streamsize size = file.tellg();
	file.seekg(0, std::ios::beg);

	if (size % sizeof(double) != 0)
		throw std::runtime_error("File size is not a multiple of sizeof(double)");

	std::vector<double> loadedData(size / sizeof(double));

	file.read(reinterpret_cast<char*>(loadedData.data()), size);

	return loadedData;
}